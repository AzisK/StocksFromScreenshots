from constants import PATTERN
from extraction import preprocess_image, extract_text_from_image

with open('sample_screenshot/sample_screenshot.jpg', 'rb') as f:
    file_bytes = f.read()

preprocess_images = preprocess_image(file_bytes)

text = extract_text_from_image(preprocess_images[-1])

matches = list(PATTERN.finditer(text))
print('Matches:')
print(matches)

for match in matches:
    print(match.groupdict())
