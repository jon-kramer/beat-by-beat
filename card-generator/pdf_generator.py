#!/usr/bin/env python3
"""
PDF Generator for Beat by Beat Cards
Converts HTML files to print-ready PDFs using Playwright
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def html_to_pdf(html_path, pdf_path):
    """Convert an HTML file to PDF using Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        await page.goto(f'file://{html_path.absolute()}')

        # Wait for content to load
        await page.wait_for_load_state('networkidle')

        # Generate PDF with print settings
        await page.pdf(
            path=str(pdf_path),
            format='Letter',
            print_background=True,
            margin={
                'top': '0',
                'right': '0',
                'bottom': '0',
                'left': '0'
            },
            prefer_css_page_size=True
        )

        await browser.close()
        print(f'Generated: {pdf_path.name}')


async def main():
    """Generate PDFs for all card HTML files"""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'output' / 'html'
    pdf_dir = base_dir / 'output' / 'pdf'

    # Create PDF directory
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # List of HTML files to convert
    html_files = [
        'starter-cards.html',
        'pool-cards.html',
        'rhythm-cards.html',
        'judge-cards.html',
        'stumble-cards.html',
        'move-backs.html',
        'rhythm-backs.html',
        'judge-backs.html',
    ]

    print('🎭 Beat by Beat - PDF Generator')
    print('=' * 40)
    print()

    # Convert each HTML file to PDF
    for html_file in html_files:
        html_path = output_dir / html_file
        if html_path.exists():
            pdf_name = html_file.replace('.html', '.pdf')
            pdf_path = pdf_dir / pdf_name
            await html_to_pdf(html_path, pdf_path)
        else:
            print(f'Warning: {html_file} not found, skipping...')

    print()
    print(f'✅ All PDFs generated in: {pdf_dir}')
    print()
    print('Print-ready PDFs:')
    print(f'  - starter-cards.pdf (2 sheets)')
    print(f'  - pool-cards.pdf (14 sheets)')
    print(f'  - rhythm-cards.pdf (9 sheets)')
    print(f'  - judge-cards.pdf (2 sheets)')
    print(f'  - stumble-cards.pdf (3 sheets)')
    print(f'  + 3 back files (move, rhythm, judge)')


if __name__ == '__main__':
    asyncio.run(main())
