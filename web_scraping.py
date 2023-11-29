import requests
from bs4 import BeautifulSoup
import argparse

class Scrap:

    def __init__(self, site_url=""):
        self.site_url = site_url
        self.site_html = ""
        self.info_list = []
        self.file_name = ""
        user_agent_content = self.get_user_agent()
        self.custom_header = {
            "user-agent": user_agent_content
        }

    # def clear_screen(self):
    #     """The function clears the screen using the command related to the operating system."""
    #     if os.name == "nt":
    #         "The operating system will be windows,so it uses the command cls"
    #         os.system("cls")
    #     else:
    #         os.system("clear")

    def validate_url(self):
        """The function Verifies if the url contains the https prefix. If not, then add the prefix to the url."""
        https_prefix = "https://"
        if https_prefix not in self.site_url:
            self.site_url = https_prefix + self.site_url


    def get_user_agent(self):
        with open("user_agent.txt", "r") as user_agent_file:
            # strip() is used to remove the newline character(\n) at the end of the string.
            user_agent = user_agent_file.readline().strip()
        return user_agent

    def get_site_html(self):

        response = requests.get(self.site_url, headers=self.custom_header)
        response.raise_for_status()
        response.encoding = "utf-8"
        self.site_html = response.text

    def get_tag_info(self):
        soup = BeautifulSoup(self.site_html, "html.parser")
        selector = input("Enter the selector: ")
        tag_list = soup.select(selector)
        for tags in tag_list:
            self.info_list.append(tags.getText())



    def write_file(self):
        print(f"[+] Saving the tag info in the file: {self.file_name}")
        with open(self.file_name, mode="w", encoding="utf-8") as info_file:
            for file_line in self.info_list:
                info_file.write(f"{file_line}\n")
        print(f"[+] File saved.")
    def handle_options(self):
        parser = argparse.ArgumentParser(
            prog="Web Scraper",
            description='command-line web scrapping program'
        )
        parser.add_argument("-g", "--get",
                            dest="site",
                            required=True,
                            help="site to get the tag info")
        parser.add_argument("-w", "--write",
                            dest="file_name",
                            required=True,
                            help="file to write the tag info")
        args = parser.parse_args()
        self.site_url = args.site
        self.file_name = args.file_name
        self.validate_url()
        try:
            self.get_site_html()
        except requests.HTTPError as httperr:
            raise SystemExit(f"[!] {httperr}")
        except requests.ConnectionError as connectionErr:
            raise SystemExit(f"[!] {connectionErr}")

        self.get_tag_info()
        try:
            if not self.info_list:
                while not self.info_list:
                    print("[!] There's no item with the selector informed. Please, try again or type ctrl+c to exit.")
                    self.get_tag_info()
        except KeyboardInterrupt:
            print("\n[!] Exiting....")
            exit()

        self.write_file()

if __name__ == "__main__":
    s = Scrap()
    s.handle_options()

