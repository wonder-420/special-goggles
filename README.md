Use bash to run the script using the following command : python organize_downloads.py
You can specify a custom downloads folder using : python organize_downloads.py --path "/path/to/your/downloads"
To list your files after organising them use :python organize_downloads.py --list
To automate the sorting use the command : # Run daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/organize_downloads.py
