#! /usr/bin/env python3

from copy import copy
from optparse import OptionParser, Option, OptionValueError
from time import sleep
import requests


welcome_msg = r"""
    ____                                                
   / __/____   _____ ____ ___   _____                   
  / /_ / __ \ / ___// __ `__ \ / ___/                   
 / __// /_/ // /   / / / / / /(__  )                    
/_/___\____//_/ __/_/_/_/_/_//____/___ ___   ___   _____
  / ___// __ \ / __ `// __ `__ \ / __ `__ \ / _ \ / ___/
 (__  )/ /_/ // /_/ // / / / / // / / / / //  __// /    
/____// .___/ \__,_//_/ /_/ /_//_/ /_/ /_/ \___//_/     
     /_/                                                

by: deciphr                                                                                                                                                  
"""

# Custom type for parsing responses
def check_entries(option, opt, value):
    entry_list = {}

    for entry in value.split(","):
        entry_split = entry.split(":")
        
        try:
            entry_id, entry_value = entry_split[0], entry_split[1]

            entry_list[f"entry.{entry_id}"] = entry_value
        except IndexError:
            raise OptionValueError(
                f"option {opt}: invalid entry syntax"
            )
        
    return entry_list

class EntryOption(Option):
    TYPES = Option.TYPES + ("entries",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["entries"] = check_entries


# Main
def submit_form(url, entries):
    # headers = {
    #     'Referer': "url",
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
    # }

    response = requests.post(f"{url[:-9]}/formResponse", data=entries)
    return response

def main():
    print(welcome_msg)

    usage = "%prog -u <url> -e <entries> [options]"
    parser = OptionParser(option_class=EntryOption, usage=usage)
    
    parser.add_option("-u", "--url",
                      help="form url to send requests to (https://docs.google.com/forms/d/e/.../viewform)")
                      
    parser.add_option("-e", "--entries", type="entries",
                      help="entries to fill out (format: id:value,...)")

    parser.add_option("-c", "--count", type="int",
                      default=1,
                      help="amount of requests to send")
    parser.add_option("-i", "--interval", type="int",
                      default=0,
                      help="number of seconds between each request")
    parser.add_option("-q", "--quiet", 
                      action="store_false", default=False,
                      help="only outputs when completed or errored")

    (options, args) = parser.parse_args(args=None, values=None)

    if options.url == None:
        parser.print_help()
        return
    else:
        url = options.url
        entries = options.entries

        if entries != None:
            success_count = 0

            count = options.count
            interval = options.interval
            
            if not options.quiet:
                print(f"Sending requests @ {count} req/{interval}s")

            for x in range(count):
                response = submit_form(url, entries)
                
                if not options.quiet:
                    print(f"[{x+1}]: {response}")

                    if response.status_code == 200:
                        success_count += 1

                sleep(interval)
            
            print(f"\nCompleted {success_count}/{count} requests!")


if __name__ == "__main__":
    main()
