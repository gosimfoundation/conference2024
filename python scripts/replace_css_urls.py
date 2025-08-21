#!/usr/bin/env python3
"""
Script to replace external URLs in CSS file with local paths
"""

import re
import os

def replace_css_urls():
    css_file = 'css/china2024.css'
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define URL mappings
    url_mappings = {
        # Background images
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a9417e544edf8ef9e5ba4e_bg%201.png': '../images/66a9417e544edf8ef9e5ba4e_bg 1.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a9417e544edf8ef9e5ba08_bg.png': '../images/66a9417e544edf8ef9e5ba08_bg.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a94180544edf8ef9e5bb62_footer%20bar.png': '../images/66a94180544edf8ef9e5bb62_footer bar.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a9417f544edf8ef9e5ba7d_attractions%20%2C%20paticipation.png': '../images/66a9417f544edf8ef9e5ba7d_attractions , paticipation.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c6b903db164920f9c9a1bd_bg-p.png': '../images/66c6b903db164920f9c9a1bd_bg-p.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c79084a771b6f7fa449bd4_bg-399.png': '../images/66c79084a771b6f7fa449bd4_bg-399.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c642a744df1a4a249c160a_Screen%20Shot%202024-08-21%20at%2012.40.06%20PM.png': '../images/66c642a744df1a4a249c160a_Screen Shot 2024-08-21 at 12.40.06 PM.png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/670fe715dbb6d0342d5edfb9_66c79084a771b6f7fa449bd4_bg-399%20(1).png': '../images/670fe715dbb6d0342d5edfb9_66c79084a771b6f7fa449bd4_bg-399 (1).png',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c8bb905168c6e405413b67_Arrow-Outward--Streamline-Rounded----Material-Symbols.svg': '../images/66c8bb905168c6e405413b67_Arrow-Outward--Streamline-Rounded----Material-Symbols.svg',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/670fe69911bbbac701be7b9a_bg-i389223.png': '../images/670fe69911bbbac701be7b9a_bg-i389223.png',
        
        # Cloudfront URLs
        'https://d3e54v103j8qbb.cloudfront.net/img/background-image.svg': '../images/background-image.svg',
        
        # Font files
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a9410330942c144ac1f66b_Sarabun-Bold.ttf': '../fonts/66a9410330942c144ac1f66b_Sarabun-Bold.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a94111587d6bd6bb42729d_Sarabun-Regular.ttf': '../fonts/66a94111587d6bd6bb42729d_Sarabun-Regular.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a9411b3289fbf359a3bd98_Sarabun-Italic.ttf': '../fonts/66a9411b3289fbf359a3bd98_Sarabun-Italic.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a941168aae459935dce597_Sarabun-Medium.ttf': '../fonts/66a941168aae459935dce597_Sarabun-Medium.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66a941091f5dc791ab5e2820_Sarabun-SemiBold.ttf': '../fonts/66a941091f5dc791ab5e2820_Sarabun-SemiBold.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c65b64c63d9dc3d9121361_HankenGrotesk-VariableFont_wght.ttf': '../fonts/66c65b64c63d9dc3d9121361_HankenGrotesk-VariableFont_wght.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c65b562d6c875276ece304_Arvo-Bold.ttf': '../fonts/Arvo-Bold.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c65b537ba186fa240a0bc3_Arvo-Italic.ttf': '../fonts/66c65b537ba186fa240a0bc3_Arvo-Italic.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c65b4fa01f3c1ba9ac6574_Arvo-Regular.ttf': '../fonts/Arvo-Regular.ttf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7cf285a4f88d5b83025_ClashDisplay-Extralight.otf': '../fonts/668dd7cf285a4f88d5b83025_ClashDisplay-Extralight.otf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7cff25ab5675d7b7930_ClashDisplay-Light.otf': '../fonts/668dd7cff25ab5675d7b7930_ClashDisplay-Light.otf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7cf5549a41cb9f6f53a_ClashDisplay-Semibold.otf': '../fonts/ClashDisplay-Semibold.otf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7cf79026593e2952f15_ClashDisplay-Medium.otf': '../fonts/ClashDisplay-Medium.otf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7cff7b900de31824c10_ClashDisplay-Bold.otf': '../fonts/668dd7cff7b900de31824c10_ClashDisplay-Bold.otf',
        'https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/668dd7d03e15017645604c6e_ClashDisplay-Regular.otf': '../fonts/ClashDisplay-Regular.otf',
    }
    
    # Replace URLs
    replaced_count = 0
    for old_url, new_url in url_mappings.items():
        # Handle both single and double quotes
        old_url_single = old_url.replace('"', "'")
        old_url_double = old_url.replace("'", '"')
        
        # Count replacements
        count_single = content.count(old_url_single)
        count_double = content.count(old_url_double)
        
        if count_single > 0:
            content = content.replace(old_url_single, f"'{new_url}'")
            replaced_count += count_single
            print(f"Replaced {count_single} instances of {old_url_single}")
            
        if count_double > 0:
            content = content.replace(old_url_double, f'"{new_url}"')
            replaced_count += count_double
            print(f"Replaced {count_double} instances of {old_url_double}")
    
    # Write the updated content back to the file
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal replacements made: {replaced_count}")
    print(f"Updated CSS file: {css_file}")

if __name__ == "__main__":
    replace_css_urls()
