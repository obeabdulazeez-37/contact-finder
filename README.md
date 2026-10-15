# Contact Finder

A command-line Python tool that takes a company domain and a department, searches the Hunter.io API for people at that company, and prints a ranked list of the most relevant contacts.

I built it to find recruiters and team members to reach out to after applying for a job. It does the first pass of the search so I can spend my time on the LinkedIn profiles that matter.

## What it does

1. Asks for a company domain (for example `example.com`) and a department (`hr` or `it`).
2. Cleans the input: removes spaces, `https://`, `www.` and any page path.
3. Sends a Domain Search request to Hunter.io with your API key.
4. Reads each contact's job title and scores it against keyword lists for the chosen department.
5. Ranks the matches and prints the top 10 with name, title, email, confidence, verification status and LinkedIn link.

## How the scoring works

Each department has three keyword lists, stored in the `keyword_sets` dictionary at the top of the script.

|        List        |       Effect       |
-------------------------------------------
| `strong`           | Title matches a strong keyword, score 2 |
| `weak`             | Title matches only a weak keyword, score 1 |
| `exclude`          | Title contains an excluded word, contact is dropped |

Matches are sorted by:

1. Score, highest first
2. Email verification status (`valid`, then `accept_all`, then unverified)
3. Hunter's confidence score, highest first

## Requirements

- Python 3.10 or newer
- The `requests` library
- A free Hunter.io account and API key

## Setup

1. Clone the repository and move into the folder:

   ```
   git clone https://github.com/<your-username>/contact-finder.git
   cd contact-finder
   ```

2. Install the dependency:

   ```
   pip install -r requirements.txt
   ```

3. Create a Hunter.io account and copy your API key from the API page of your dashboard.

4. In the project folder, create a file named `API_key.txt` that contains only your key. This file is listed in `.gitignore` and should never be committed.

## Usage

```
python contact_finder.py
```

Example run (the data below is made up):

```
Enter company's domain: https://www.example.com/
Enter department you would love to filter through: hr
Good status: 200
Search finished!
Showing 2 of 2 contacts at example.com (hr)
Jane Doe | Senior Talent Acquisition Specialist | jdoe@example.com | 88 | valid | https://www.linkedin.com/in/jane-doe-example
Sam Lee | HR Advisor | slee@example.com | 74 | unverified | none
```

## Customizing the keywords

To change what counts as a match, edit the lists in `keyword_sets`. To add a department, add a new key with its own `strong`, `weak` and `exclude` lists. The department name must also be one Hunter accepts as a filter.

## Limitations

- Many emails returned by Hunter are generated from a company's email pattern rather than found on a page, so some will be wrong. Check the verification status before using one.
- Job titles come from Hunter's data and may be out of date.
- Keywords are matched as plain text, so short keywords can match inside longer words (for example `soc` inside `associate`).
- Only the `hr` and `it` departments have keyword lists so far.
- The tool does not check schools or alumni connections. Use the LinkedIn links to do that yourself.
- Each search uses Hunter credits, and the free plan has a monthly allowance.

## Roadmap

- Match whole words only
- Page through more than one set of results
- Export results to CSV
- Add more departments
- Move the keyword lists into a separate file
- Read the API key from an environment variable
- Show remaining Hunter credits after each search

## Responsible use

This tool works with publicly available business contact data. Use it to send a small number of relevant, personal messages, not bulk outreach. Follow Hunter.io's terms of service and the anti-spam and privacy laws that apply where you and the recipient live.

## Built with

- Python
- [Hunter.io API](https://hunter.io/api-documentation)
- `requests`
