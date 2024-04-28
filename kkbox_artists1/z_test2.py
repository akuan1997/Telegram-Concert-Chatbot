# from fuzzywuzzy import fuzz
#
# sim = fuzz.ratio('寶兒', 'BoA 寶兒')
# print(sim)

# with open('japanese_link.txt', 'r', encoding='utf-8') as f:
#     japanese_lines = f.readlines()
# japanese_lines = [line.replace('\n', '') for line in japanese_lines]
#
# with open('korean_link.txt', 'r', encoding='utf-8') as f:
#     korean_lines = f.readlines()
# korean_lines = [line.replace('\n', '') for line in korean_lines]
#
# for japanese_line in japanese_lines:
#     for korean_line in korean_lines:
#         japanese_name = japanese_line.split('/')[-1]
#         korean_name = korean_line.split('/')[-1]
#         if japanese_name == korean_name:
#             print(japanese_line)
#             print('---')

# Read the original file
with open('all_links.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Dictionary to hold unique entries
unique_urls = {}

# Process each line
for line in lines:
    # Split to get the name and the URL
    parts = line.strip().split('|||')
    if len(parts) < 2:
        continue  # Skip any malformed lines

    name, url = parts[0], parts[1]
    # Split URL by '/' and get the last segment
    last_segment = url.split('/')[-1]

    # Check if the last segment already exists in the dictionary
    if last_segment not in unique_urls:
        unique_urls[last_segment] = line.strip()  # Store the entire line

# Write the unique URLs to a new file
with open('all_links1.txt', 'w', encoding='utf-8') as output_file:
    for url in unique_urls.values():
        output_file.write(url + '\n')

print("Unique URLs have been written to all_links1.txt.")
