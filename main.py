import subprocess


if __name__ == '__main__':
    args = ('zip', '-r', '-', 'photos', '-1')
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stdin=None,
                               stderr=subprocess.PIPE)
    archive, stderr = process.communicate()
    with open('archive.zip', 'wb') as zip_file:
        zip_file.write(archive)
