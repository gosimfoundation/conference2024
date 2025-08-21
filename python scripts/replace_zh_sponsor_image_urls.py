#!/usr/bin/env python3
"""
Script to replace external CDN image URLs with local asset paths in zh/sponsors.html
"""

import re
import os

def replace_image_urls():
    # Define the mapping of external URLs to local paths (adjusted for zh/ directory)
    url_mapping = {
        # CSDN Logo
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/667c4f10c5b167f98e5d000f_64d465bcc7f9c0552d22bfe1_CSDN_Logo\.svg': '../images/667c4f10c5b167f98e5d000f_64d465bcc7f9c0552d22bfe1_CSDN_Logo.svg',
        
        # Futurewei
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/667c4f10611c4fa11bf1752e_futurewei\.svg': '../images/667c4f10611c4fa11bf1752e_futurewei.svg',
        
        # Baai
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c30a710ce82bc0223e_Baai\.png': '../images/66fdb4c30a710ce82bc0223e_Baai.png',
        
        # Airs
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3d6c2d2e8a3b7765e_airs\.png': '../images/66fdb4c3d6c2d2e8a3b7765e_airs.png',
        
        # Gitcode
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c308dfce331d236e96_gitcode\.png': '../images/66fdb4c308dfce331d236e96_gitcode.png',
        
        # Khronos
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2110c0c318f4b6e4f_khronos\.png': '../images/66fdb4c2110c0c318f4b6e4f_khronos.png',
        
        # Non-covex
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2ab314ae4d3a62acc_non\-covex\.png': '../images/66fdb4c2ab314ae4d3a62acc_non-covex.png',
        
        # Relevant
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c27f1631bf41acc236_relevant\.png': '../images/66fdb4c27f1631bf41acc236_relevant.png',
        
        # MeetKai
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3f6de0c8efb5133a3_MeetKai\.png': '../images/66fdb4c3f6de0c8efb5133a3_MeetKai.png',
        
        # Eclipse
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3cb0ae6961f113b12_eclipse\.png': '../images/66fdb4c3cb0ae6961f113b12_eclipse.png',
        
        # Rust Foundation
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3d65865f449e3f8b9_rustfoundation\.png': '../images/66fdb4c3d65865f449e3f8b9_rustfoundation.png',
        
        # Tweedegold
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c28ce71f7045bd0451_tweedegold\.png': '../images/66fdb4c28ce71f7045bd0451_tweedegold.png',
        
        # Matrix
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2b54fd78d202a00fc_matrix\.png': '../images/66fdb4c2b54fd78d202a00fc_matrix.png',
        
        # Metaverse
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2e66529d6e47a258b_metaverse\.png': '../images/66fdb4c2e66529d6e47a258b_metaverse.png',
        
        # Moxin Logo
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdbc8df2556057c33f54e4_moxin\-logo\.svg': '../images/66fdbc8df2556057c33f54e4_moxin-logo.svg',
        
        # Wasmedge
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2cca869543d27f2f6_wasmedge\.png': '../images/66fdb4c2cca869543d27f2f6_wasmedge.png',
        
        # Trifecta
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c25e27fbd31a1ae5e2_trifecta\.png': '../images/66fdb4c25e27fbd31a1ae5e2_trifecta.png',
        
        # Generative AI Commons
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3e60d3a7301acdd0b_generativeaicommons\.png': '../images/66fdb4c3e60d3a7301acdd0b_generativeaicommons.png',
        
        # Rust Week
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2260d08af5dbb2a6c_rust\-week\.png': '../images/66fdb4c2260d08af5dbb2a6c_rust-week.png',
        
        # Xlang
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c2623706f37c98f5c7_Xlang\.png': '../images/66fdb4c2623706f37c98f5c7_Xlang.png',
        
        # Second State
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c243cb17ec822eeaf8_second\-state\.svg': '../images/66fdb4c243cb17ec822eeaf8_second-state.svg',
        
        # OPU
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c218572cc9c7a2f690_opu\.png': '../images/66fdb4c218572cc9c7a2f690_opu.png',
        
        # Silicon Flow
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c243cb17ec822eeb50_silicon\-flow\.png': '../images/66fdb4c243cb17ec822eeb50_silicon-flow.png',
        
        # Kaiyuanshe
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c36c6ef8c0637be898_kaiyuanshe\.png': '../images/66fdb4c36c6ef8c0637be898_kaiyuanshe.png',
        
        # LlamaEdge
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb5eec8f0d1c66f2986af_llamaedge\-with\-black\.svg': '../images/66fdb5eec8f0d1c66f2986af_llamaedge-with-black.svg',
        
        # OpenBayes
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb4c3f6de0c8efb5133ec_openbayes\.svg': '../images/66fdb4c3f6de0c8efb5133ec_openbayes.svg',
        
        # DeveloperG
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb87dd94c2d1f6ea6d334_developerg\-3\.svg': '../images/66fdb87dd94c2d1f6ea6d334_developerg-3.svg',
        
        # Tsing
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66fdb7864a335ccb741ad517_tsing\.png': '../images/66fdb7864a335ccb741ad517_tsing.png',
        
        # Sponsor Image
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c78bf07cb8d237c6ababe0_sponsor\-img\.png': '../images/66c78bf07cb8d237c6ababe0_sponsor-img.png',
        
        # AI New Spark Icon
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66a9a049355b9698c78c3227_Ai\-New\-Spark\-\-Streamline\-Plump\-Remix\.svg': '../images/66a9a049355b9698c78c3227_Ai-New-Spark--Streamline-Plump-Remix.svg',
        
        # Crown Icon
        '\.\./\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66a9a068a74c0b0fb8290586_Crown\-\-Streamline\-Plump\-Remix\.svg': '../images/66a9a068a74c0b0fb8290586_Crown--Streamline-Plump-Remix.svg',
    }
    
    # Read the zh/sponsors.html file
    with open('zh/sponsors.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Track replacements
    replacements_made = 0
    
    # Perform replacements
    for external_url, local_path in url_mapping.items():
        # Check if the local file exists (adjust path for zh/ directory)
        local_file_path = local_path.replace('../images/', 'images/')
        if os.path.exists(local_file_path):
            # Use regex to replace the URL
            if re.search(external_url, content):
                content = re.sub(external_url, local_path, content)
                replacements_made += 1
                print(f"Replaced: {external_url} -> {local_path}")
        else:
            print(f"Warning: Local file not found: {local_file_path}")
    
    # Write the updated content back to the file
    with open('zh/sponsors.html', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"\nTotal replacements made: {replacements_made}")
    print("zh/sponsors.html has been updated successfully!")

if __name__ == "__main__":
    replace_image_urls()
