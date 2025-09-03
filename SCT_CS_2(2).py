from PIL import Image
import random
import numpy as np
import json

# Load the image and convert to RGB if needed
def load_image(path):
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img

# Apply XOR encryption/decryption to each pixel using numpy for speed
def xor_pixels(image, key=123):
    arr = np.array(image)
    arr ^= key
    return Image.fromarray(arr)

# Swap pixels randomly (basic shuffle)
def swap_pixels(image, seed=42):
    random.seed(seed)
    pixels = list(image.getdata())
    indices = list(range(len(pixels)))
    random.shuffle(indices)

    new_pixels = [pixels[i] for i in indices]
    swapped_image = Image.new("RGB", image.size)
    swapped_image.putdata(new_pixels)

    return swapped_image, indices  # return indices to reverse it

# Reverse the pixel swap
def unswap_pixels(image, indices):
    pixels = list(image.getdata())
    unswapped = [None] * len(pixels)

    for i, index in enumerate(indices):
        unswapped[index] = pixels[i]

    original_image = Image.new("RGB", image.size)
    original_image.putdata(unswapped)

    return original_image

# Save indices to a JSON file
def save_indices(indices, path):
    with open(path, 'w') as f:
        json.dump(indices, f)

# Load indices from a JSON file
def load_indices(path):
    with open(path, 'r') as f:
        indices = json.load(f)
    return indices

# Example usage
if __name__ == "__main__":
    input_path = "2025-09-02 (2).png"
    encrypted_path = "encrypted_image.png"
    decrypted_path = "decrypted_image.png"
    indices_path = "shuffle_indices.json"
    key = 99
    seed = 42

    # Load original image
    original = load_image(input_path)

    # Encrypt
    xor_encrypted = xor_pixels(original, key=key)
    swapped_image, swap_indices = swap_pixels(xor_encrypted, seed=seed)
    swapped_image.save(encrypted_path)
    save_indices(swap_indices, indices_path)
    print(f"Encrypted image saved as {encrypted_path}")
    print(f"Shuffle indices saved as {indices_path}")

    # Decrypt
    loaded_indices = load_indices(indices_path)
    unswapped_image = unswap_pixels(swapped_image, loaded_indices)
    decrypted_image = xor_pixels(unswapped_image, key=key)  # same key
    decrypted_image.save(decrypted_path)
    print(f"Decrypted image saved as {decrypted_path}")
