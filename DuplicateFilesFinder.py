import os
import hashlib
from shutil import move


def md5(fname):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicates_in_directory(directory):
    """Find duplicate files based on their MD5 hash."""
    seen_hashes = {}
    duplicates = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            filehash = md5(filepath)

            if filehash in seen_hashes:
                duplicates.append((filepath, seen_hashes[filehash]))
            else:
                seen_hashes[filehash] = filepath

    return duplicates


def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    duplicates_directory = os.path.join(current_directory, "duplicates")

    # Create duplicates directory if it doesn't exist
    if not os.path.exists(duplicates_directory):
        os.mkdir(duplicates_directory)

    duplicates = find_duplicates_in_directory(current_directory)

    print("=" * 60)
    print("DUPLICATE FILES DETECTED")
    print("=" * 60 + "\n")

    for dup_path, orig_path in duplicates:
        print(f"Original: {orig_path}")
        print(f"Duplicate: {dup_path}")

        # Move the duplicate file to the duplicates directory
        base_name = os.path.basename(dup_path)
        new_path = os.path.join(duplicates_directory, base_name)

        # Handle possible name conflicts in the duplicates folder
        counter = 1
        while os.path.exists(new_path):
            base_name_without_extension, extension = os.path.splitext(base_name)
            new_path = os.path.join(duplicates_directory, f"{base_name_without_extension}_{counter}{extension}")
            counter += 1

        move(dup_path, new_path)
        print(f"Moved to: {new_path}")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
