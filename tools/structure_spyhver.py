#!/usr/bin/env python3
"""
Asset Counter for Git Repository
Analyzes project structure to help plan spyhver message placement
"""

import os
import json
import mimetypes
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

class AssetCounter:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': defaultdict(int),
            'by_category': defaultdict(int),
            'by_directory': defaultdict(int),
            'file_sizes': [],
            'potential_carriers': []
        }
        
        # Define categories for different file types
        self.categories = {
            'code': {'.py', '.js', '.html', '.css', '.json', '.md', '.txt', '.yml', '.yaml'},
            'image': {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico'},
            'audio': {'.mp3', '.wav', '.ogg', '.m4a', '.flac'},
            'video': {'.mp4', '.avi', '.mkv', '.mov', '.webm'},
            'data': {'.json', '.xml', '.csv', '.db', '.sqlite'},
            'config': {'.gitignore', '.env', '.ini', '.conf', '.cfg'},
            'documentation': {'.md', '.rst', '.txt', '.pdf', '.doc', '.docx'}
        }
        
        # Files/dirs to ignore
        self.ignore_patterns = {
            '.git', '__pycache__', 'node_modules', '.pytest_cache',
            '.venv', 'venv', 'env', '.env', 'dist', 'build',
            '*.pyc', '*.pyo', '.DS_Store', 'Thumbs.db'
        }
        
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        parts = path.parts
        name = path.name
        
        # Check exact matches and patterns
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in parts or name == pattern:
                return True
                
        return False
    
    def categorize_file(self, file_path: Path) -> str:
        """Categorize file by extension"""
        ext = file_path.suffix.lower()
        
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
                
        return 'other'
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for spyhver potential"""
        try:
            size = file_path.stat().st_size
            ext = file_path.suffix.lower()
            category = self.categorize_file(file_path)
            
            analysis = {
                'path': str(file_path),
                'size': size,
                'extension': ext,
                'category': category,
                'lines': 0,
                'characters': 0,
                'words': 0,
                'spyhver_capacity': 0
            }
            
            # For text files, count lines and estimate capacity
            if category in ['code', 'documentation', 'data']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        analysis['lines'] = content.count('\n') + 1
                        analysis['characters'] = len(content)
                        analysis['words'] = len(content.split())
                        
                        # Estimate spyhver capacity based on content
                        # Comments in code files
                        if ext == '.py':
                            analysis['spyhver_capacity'] = content.count('#') + content.count('"""')
                        elif ext in ['.js', '.css', '.java', '.c', '.cpp']:
                            analysis['spyhver_capacity'] = content.count('//') + content.count('/*')
                        elif ext == '.html':
                            analysis['spyhver_capacity'] = content.count('<!--')
                        # Whitespace potential
                        analysis['spyhver_capacity'] += content.count('  ') // 10  # Double spaces
                        
                except:
                    pass
            
            # Binary files have different capacity
            elif category == 'image':
                # Images can hide data in LSB
                analysis['spyhver_capacity'] = size // 8  # Rough estimate
                
            return analysis
            
        except Exception as e:
            return None
    
    def scan_directory(self, directory: Path = None) -> None:
        """Recursively scan directory structure"""
        if directory is None:
            directory = self.root_path
            
        try:
            for item in directory.iterdir():
                if self.should_ignore(item):
                    continue
                    
                if item.is_dir():
                    self.stats['total_dirs'] += 1
                    self.stats['by_directory'][str(item.relative_to(self.root_path))] += 1
                    self.scan_directory(item)
                    
                elif item.is_file():
                    self.stats['total_files'] += 1
                    
                    # Analyze file
                    file_analysis = self.analyze_file(item)
                    if file_analysis:
                        self.stats['total_size'] += file_analysis['size']
                        self.stats['by_extension'][file_analysis['extension']] += 1
                        self.stats['by_category'][file_analysis['category']] += 1
                        self.stats['file_sizes'].append(file_analysis['size'])
                        
                        # Track files with good spyhver potential
                        if file_analysis['spyhver_capacity'] > 50:
                            self.stats['potential_carriers'].append(file_analysis)
                            
        except PermissionError:
            pass
    
    def calculate_statistics(self) -> Dict:
        """Calculate additional statistics"""
        if self.stats['file_sizes']:
            self.stats['average_file_size'] = sum(self.stats['file_sizes']) // len(self.stats['file_sizes'])
            self.stats['largest_file'] = max(self.stats['file_sizes'])
            self.stats['smallest_file'] = min(self.stats['file_sizes'])
        
        # Sort potential carriers by capacity
        self.stats['potential_carriers'].sort(key=lambda x: x['spyhver_capacity'], reverse=True)
        
        return self.stats
    
    def format_size(self, size: int) -> str:
        """Format byte size to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def generate_report(self) -> str:
        """Generate detailed report for spyhver planning"""
        report = []
        report.append("=" * 60)
        report.append("ASSET ANALYSIS REPORT FOR SPYHVER PLANNING")
        report.append("=" * 60)
        report.append("")
        
        # Overview
        report.append("OVERVIEW:")
        report.append(f"  Total Files: {self.stats['total_files']:,}")
        report.append(f"  Total Directories: {self.stats['total_dirs']:,}")
        report.append(f"  Total Size: {self.format_size(self.stats['total_size'])}")
        report.append("")
        
        # By Category
        report.append("FILES BY CATEGORY:")
        for category, count in sorted(self.stats['by_category'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {category:15} {count:5} files")
        report.append("")
        
        # By Extension
        report.append("TOP FILE EXTENSIONS:")
        ext_sorted = sorted(self.stats['by_extension'].items(), key=lambda x: x[1], reverse=True)[:10]
        for ext, count in ext_sorted:
            ext_display = ext if ext else "(no extension)"
            report.append(f"  {ext_display:15} {count:5} files")
        report.append("")
        
        # Directory Structure
        report.append("MAIN DIRECTORIES:")
        dir_sorted = sorted(self.stats['by_directory'].items(), key=lambda x: x[1], reverse=True)[:10]
        for dir_name, count in dir_sorted:
            if dir_name:  # Skip root
                report.append(f"  {dir_name:30} {count:5} items")
        report.append("")
        
        # Spyhver Recommendations
        report.append("SPYHVER CARRIER RECOMMENDATIONS:")
        report.append("(Files with highest hiding capacity)")
        report.append("")
        
        for i, carrier in enumerate(self.stats['potential_carriers'][:15], 1):
            report.append(f"{i}. {carrier['path']}")
            report.append(f"   Category: {carrier['category']}")
            report.append(f"   Size: {self.format_size(carrier['size'])}")
            if carrier['lines'] > 0:
                report.append(f"   Lines: {carrier['lines']:,}")
            report.append(f"   Estimated Capacity: {carrier['spyhver_capacity']} units")
            report.append("")
        
        # Calculate total message capacity
        total_capacity = sum(c['spyhver_capacity'] for c in self.stats['potential_carriers'])
        total_chars = sum(c['characters'] for c in self.stats['potential_carriers'])
        
        report.append("TOTAL SPYHVER CAPACITY:")
        report.append(f"  Total hiding spots: {total_capacity:,}")
        report.append(f"  Total characters in text files: {total_chars:,}")
        report.append(f"  Recommended message length: {total_capacity // 10} characters")
        report.append(f"  Maximum stealth message: {total_capacity // 100} characters")
        report.append("")
        
        # Steganography strategies
        report.append("SUGGESTED SPYHVER STRATEGIES:")
        report.append("1. Comment Injection: Add meaningful comments in code files")
        report.append("2. Whitespace Encoding: Use trailing spaces and blank lines")
        report.append("3. Variable Naming: Encode message in variable/function names")
        report.append("4. Documentation: Hide in README.md or docstrings")
        report.append("5. Metadata: Use file timestamps or git commit messages")
        report.append("6. Asset Naming: Encode in filenames following a pattern")
        report.append("7. Configuration: Hide in JSON/YAML structure")
        report.append("")
        
        return "\n".join(report)
    
    def export_data(self, filename: str = "asset_analysis.json") -> None:
        """Export detailed data for further analysis"""
        export_data = {
            'summary': {
                'total_files': self.stats['total_files'],
                'total_dirs': self.stats['total_dirs'],
                'total_size': self.stats['total_size'],
                'total_capacity': sum(c['spyhver_capacity'] for c in self.stats['potential_carriers'])
            },
            'by_category': dict(self.stats['by_category']),
            'by_extension': dict(self.stats['by_extension']),
            'top_carriers': self.stats['potential_carriers'][:50]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Detailed analysis exported to {filename}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze git repository assets for spyhver planning')
    parser.add_argument('path', nargs='?', default='.', help='Path to git repository (default: current directory)')
    parser.add_argument('--export', action='store_true', help='Export detailed JSON analysis')
    parser.add_argument('--output', default='asset_analysis.json', help='Output filename for JSON export')
    
    args = parser.parse_args()
    
    print(f"Analyzing repository at: {os.path.abspath(args.path)}")
    print("This may take a moment...\n")
    
    # Run analysis
    counter = AssetCounter(args.path)
    counter.scan_directory()
    counter.calculate_statistics()
    
    # Generate and print report
    report = counter.generate_report()
    print(report)
    
    # Export if requested
    if args.export:
        counter.export_data(args.output)
    
    # Additional tips
    print("\nSPYHVER ENCODING TIPS:")
    print("- Use consistent patterns across files")
    print("- Leverage git commit messages for time-based reveals")
    print("- Consider frequency analysis resistance")
    print("- Test extraction scripts separately")
    print("- Document your scheme (secretly!)")


if __name__ == "__main__":
    main()