from bs4 import BeautifulSoup
import requests
import argparse
from typing import List


def write_file(output_file: str, file_mode: str, file_contents: List[str]) -> None:
    """
    Writes the content of file_contents in the output_file.

    :param output_file: file to write the content.
    :param file_mode: the mode which the file will be open.
    :param file_contents: the list of contents to save in the file.
    :return: None.
    """
    print(f"[+] Writing the contents to file {output_file}")
    with open(output_file, mode=file_mode, encoding="utf-8") as output_file_obj:
        for file_line in file_contents:
            output_file_obj.write(f"{file_line}\n")
    print(f"[+] Writing completed.\n")


def read_file(input_file: str) -> str:
    """
    Gets the content of file input_file and returns it.

    :param input_file: the file path with the contents to read.
    :return: the file content.
    """
    try:
        print(f"[+] Getting content from file {input_file}")
        with open(input_file, "r", encoding="utf-8") as input_file_obj:
            file_content = input_file_obj.read()
        print(f"[+] File content got.\n")
        return file_content
    except FileNotFoundError:
        raise SystemExit(f"[!] file with the name {input_file} not found\n")


class Scraping:
    # Default tag file name.
    TAG_INFO_FILE = "tag_info_file.txt"
    # Default user agent file name.
    USER_AGENT_FILENAME = "user_agent.txt"

    def __init__(self):
        # the html content of the page or file.
        self.site_html = ""
        # the list of information extract from the html.
        self.info_list = []
        # the user agent that will be used in the get request header.
        self.user_agent = ""

    def get_user_agent(self) -> str | None:
        """
        Opens the user agent file, self.USER_AGENT_FILENAME, and get that information to use in the get request header.

        :return: The user-agent stored in the file or None if the file does not exist.
        """
        try:
            with open(self.USER_AGENT_FILENAME, "r") as user_agent_file:
                # strip() is used to remove the newline character(\n) at the end of the string.
                user_agent = user_agent_file.readline().strip()
            return user_agent
        except FileNotFoundError:
            print(f"[!] File {self.USER_AGENT_FILENAME} not found. Using default user agent.\n")
            return None

    def get_site_html(self, site_url: str):
        """Makes an HTTP get request to the site informed in site_url.

        :param site_url: the site to send a get request.
        :return: None.
        """
        # Verify if the site_url has the https:// prefix.
        https_prefix = "https://"
        if https_prefix not in site_url:
            site_url = https_prefix + site_url

        # Get the user_agent that will be used in the get request header.
        custom_user_agent = self.get_user_agent()
        if custom_user_agent:
            custom_header = {
                "user-agent": custom_user_agent
            }
        else:
            print(f"[!] User agent not found in the file. Using default user agent.\n")
            custom_header = None
        try:
            # Make a get requests for the specified site and receive the response.
            print(f"[+] Requesting page {site_url}")
            response = requests.get(site_url, headers=custom_header)
            print("[+] Page returned.\n")
            # Raise requests.HTTPError if the HTTP request returned an unsuccessful status code.
            response.raise_for_status()
            # Set the encoding to be used when calling response.text.
            response.encoding = "utf-8"
            self.site_html = response.text

        except requests.HTTPError as httperr:
            raise SystemExit(f"[!] http error: \n {httperr}")
        except requests.ConnectionError as connectionErr:
            raise SystemExit(f"[!] Connection error: \n {connectionErr}")
        except requests.Timeout as timeout:
            raise SystemExit(f"[!] Timeout error: {timeout}")

    def get_file_html(self, filename: str) -> None:
        """
        Gets the html content in the file and save in self.site_html.

        :param filename: file to read.
        :return: None.
        """
        self.site_html = read_file(filename)

    def get_tag_info(self) -> None:
        """
        Gets the information in the tag that matches the css selector informed.

        :return: None.
        """
        # Creates a soup object to retrieve the information of the tags.

        soup = BeautifulSoup(self.site_html, "html.parser")
        while not self.info_list:
            # Gets the css selector to use.
            selector = input("Enter the css selector to extract the tag information: ")
            # Extracts all the tags that matches the css selector.
            tag_list = soup.select(selector)
            # Creates a list with the data in the tags.
            self.info_list = [tag.getText() for tag in tag_list]
            # If self.info_list is an empty list, then there is no tag that matches the selectors informed.
            if not self.info_list:
                print("[!] There's no tag that matches the selector informed. "
                      "Please, review the selector and try again or type ctrl+c to exit.")

    def save_tag_content(self, file_path: str) -> None:
        write_file(output_file=file_path, file_mode="w", file_contents=self.info_list)

    def handle_options(self) -> None:
        """
        Handles the command-line arguments and calls the methods to execute the command-line argument action.

        :return: None
        """
        try:
            # Creates an argument parser object to handle the command-line arguments.
            parser = argparse.ArgumentParser(
                prog="Web Scraper",
                description='command-line web scrapping program')
            parser.add_argument("-g", "--g",
                                dest="site",
                                help="site to get the html tag information.")
            parser.add_argument("-f", "--file",
                                dest="file",
                                help="file to get the html tag information."
                                )
            parser.add_argument("-o", "--output",
                                dest="output_file",
                                help="file to write the tag information.",
                                default=self.TAG_INFO_FILE)

            # Get a Namespace object with the command-line arguments as attributes.
            args = parser.parse_args()
            if args.site:
                self.get_site_html(args.site)
            elif args.file:
                self.get_file_html(args.file)
            else:
                raise SystemError("[!] Please, specify a site or file to get the html tags information.")
            # Extract the tag information from the html content.
            self.get_tag_info()
            # Save the tag information in the file.
            self.save_tag_content(args.output_file)
        except KeyboardInterrupt:
            print("\n[+] Exiting..\n")


if __name__ == "__main__":
    scraping_obj = Scraping()
    scraping_obj.handle_options()
