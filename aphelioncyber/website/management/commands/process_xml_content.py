import xml.etree.ElementTree as ET
import os
import re
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify
from aphelioncyber.website.models import ServicePageContent, XMLContentImport
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process XML files and update service page content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Specific XML file to process',
        )
        parser.add_argument(
            '--directory',
            type=str,
            default='attached_assets',
            help='Directory to scan for XML files (default: attached_assets)',
        )
        parser.add_argument(
            '--auto-watch',
            action='store_true',
            help='Watch for file changes and auto-process',
        )

    def handle(self, *args, **options):
        if options['file']:
            self.process_single_file(options['file'])
        elif options['auto_watch']:
            self.watch_directory(options['directory'])
        else:
            self.process_directory(options['directory'])

    def process_directory(self, directory):
        """Process all XML files in the specified directory"""
        if not os.path.exists(directory):
            raise CommandError(f"Directory {directory} does not exist")
        
        xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]
        
        if not xml_files:
            self.stdout.write(self.style.WARNING(f"No XML files found in {directory}"))
            return
        
        self.stdout.write(f"Found {len(xml_files)} XML files to process")
        
        for xml_file in xml_files:
            file_path = os.path.join(directory, xml_file)
            self.process_single_file(file_path)

    def process_single_file(self, file_path):
        """Process a single XML file"""
        if not os.path.exists(file_path):
            raise CommandError(f"File {file_path} does not exist")
        
        # Create import record
        import_record = XMLContentImport.objects.create(
            file_name=os.path.basename(file_path),
            file_path=file_path,
            processing_status='processing'
        )
        
        try:
            self.stdout.write(f"Processing {file_path}...")
            
            # Parse XML and extract content
            content_data = self.parse_xml_file(file_path)
            
            if content_data:
                # Create or update service page content
                page_content, created = ServicePageContent.objects.update_or_create(
                    slug=content_data['slug'],
                    defaults={
                        'title': content_data['title'],
                        'description': content_data['description'],
                        'content_data': content_data['content'],
                        'xml_source_file': os.path.basename(file_path),
                    }
                )
                
                # Update import record
                import_record.processing_status = 'completed'
                import_record.processed_at = timezone.now()
                if created:
                    import_record.pages_created = 1
                else:
                    import_record.pages_updated = 1
                import_record.save()
                
                action = "Created" if created else "Updated"
                self.stdout.write(
                    self.style.SUCCESS(f"{action} service page: {page_content.title}")
                )
            else:
                import_record.processing_status = 'failed'
                import_record.error_message = "No valid content found in XML"
                import_record.save()
                self.stdout.write(
                    self.style.ERROR(f"No valid content found in {file_path}")
                )
                
        except Exception as e:
            import_record.processing_status = 'failed'
            import_record.error_message = str(e)
            import_record.save()
            self.stdout.write(
                self.style.ERROR(f"Error processing {file_path}: {str(e)}")
            )

    def parse_xml_file(self, file_path):
        """Parse WordPress XML export and extract structured content"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find the item element (WordPress post/page)
            items = root.findall('.//item')
            if not items:
                return None
            
            item = items[0]  # Take the first item
            
            # Extract basic information
            title_elem = item.find('title')
            link_elem = item.find('link')
            content_elem = item.find('.//{http://purl.org/rss/1.0/modules/content/}encoded')
            
            if title_elem is None or content_elem is None:
                return None
            
            # Handle CDATA content properly
            title = self.get_text_content(title_elem) or ""
            link = link_elem.text if link_elem is not None else ""
            content = self.get_text_content(content_elem) or ""
            
            # Extract slug from link or generate from title
            slug = self.extract_slug_from_link(link) or slugify(title)
            
            # Parse the HTML content and extract structured data
            structured_content = self.parse_html_content(content)
            
            return {
                'title': title,
                'slug': slug,
                'description': structured_content.get('description', ''),
                'content': structured_content
            }
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def extract_slug_from_link(self, link):
        """Extract slug from WordPress link"""
        if not link:
            return None
        
        # Extract the path from URL and remove trailing slash
        match = re.search(r'/([^/]+)/?$', link.rstrip('/'))
        if match:
            return match.group(1)
        return None

    def parse_html_content(self, html_content):
        """Parse HTML content and extract structured information"""
        # Clean up the HTML content
        html_content = re.sub(r'<\s*img[^>]*>', '', html_content)  # Remove img tags
        html_content = re.sub(r'<\s*svg[^>]*>.*?</svg>', '', html_content, flags=re.DOTALL)  # Remove SVG
        
        structured_data = {
            'sections': [],
            'benefits': [],
            'solutions': [],
            'process_steps': [],
            'statistics': []
        }
        
        # Extract main description (first paragraph after title)
        desc_match = re.search(r'<h2[^>]*>.*?</h2>\s*([^<]+)', html_content)
        if desc_match:
            structured_data['description'] = desc_match.group(1).strip()
        
        # Extract benefits (list items)
        benefit_pattern = r'<li[^>]*>\s*(?:<[^>]*>)*\s*([^<]+?)(?:\s*</[^>]*>)*\s*</li>'
        benefits = re.findall(benefit_pattern, html_content)
        structured_data['benefits'] = [benefit.strip() for benefit in benefits if benefit.strip()]
        
        # Extract headings and sections
        heading_pattern = r'<h([23])[^>]*>(.*?)</h[23]>'
        headings = re.findall(heading_pattern, html_content)
        
        for level, heading_text in headings:
            heading_clean = re.sub(r'<[^>]*>', '', heading_text).strip()
            if heading_clean and not heading_clean.lower().startswith('what is'):
                structured_data['sections'].append({
                    'title': heading_clean,
                    'level': int(level)
                })
        
        # Extract solutions (h3 headings with descriptions)
        solution_pattern = r'<h3[^>]*>\s*([^<]+)\s*</h3>\s*([^<]+)'
        solutions = re.findall(solution_pattern, html_content)
        for title, desc in solutions:
            structured_data['solutions'].append({
                'title': title.strip(),
                'description': desc.strip()
            })
        
        # Extract process steps (numbered sections)
        process_pattern = r'<h3[^>]*>\s*([^<]*(?:Collection|Analysis|Generation|Assessment)[^<]*)\s*</h3>\s*<p[^>]*>\s*([^<]+)'
        process_steps = re.findall(process_pattern, html_content)
        for title, desc in process_steps:
            structured_data['process_steps'].append({
                'title': title.strip(),
                'description': desc.strip()
            })
        
        # Extract statistics (percentage values)
        stat_pattern = r'<h2[^>]*>\s*([^<]*(?:Risk|Business|Loss)[^<]*)\s*</h2>\s*([^<]+)'
        statistics = re.findall(stat_pattern, html_content)
        for title, desc in statistics:
            structured_data['statistics'].append({
                'title': title.strip(),
                'description': desc.strip()
            })
        
        return structured_data

    def get_text_content(self, element):
        """Get text content from element, handling CDATA properly"""
        if element is None:
            return ""
        
        # Get all text content including CDATA
        return element.text or ""

    def watch_directory(self, directory):
        """Watch directory for changes and auto-process new XML files"""
        self.stdout.write(f"Watching {directory} for XML file changes...")
        self.stdout.write("Press Ctrl+C to stop watching")
        
        try:
            import time
            processed_files = set()
            
            while True:
                xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]
                
                for xml_file in xml_files:
                    file_path = os.path.join(directory, xml_file)
                    file_mtime = os.path.getmtime(file_path)
                    file_key = f"{xml_file}_{file_mtime}"
                    
                    if file_key not in processed_files:
                        self.stdout.write(f"Detected new/changed file: {xml_file}")
                        self.process_single_file(file_path)
                        processed_files.add(file_key)
                
                time.sleep(2)  # Check every 2 seconds
                
        except KeyboardInterrupt:
            self.stdout.write("\nStopped watching for file changes")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Watch error: {str(e)}"))