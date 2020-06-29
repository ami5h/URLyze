
URLyze
=======


URLyze is a convenient tool to speed up your recon process.  

## Installation

Make sure you have python 3.8 and pip installed.

- Download the repository:  
`$ git clone https://github.com/ami5h/urlyze`

- Install requirements:  
`$ pip3 install requirements.txt`

- If you want to run it from anywhere in your shell:
```bash
$ cd urlyze
$ mkdir -p $HOME/.local/bin
$ echo "export PATH=$PATH:$HOME/.local/.bin" >> $HOME/.profile
$ source $HOME/.profile
$ ln -s $(pwd)/urlyze.py $HOME/.local/.bin/urlyze
$ urlyze -i input.txt -o output.txt
```

## Usage

With input file:  
`$ python3 urlyze.py -i input.txt -o output.txt`

Input through pipe and output in STDOUT:  
`$ cat urls.txt | python3 urlyze.py`

Only output URLs with status code 200 and 404:  
`$ cat urls.txt | python3 urlyze.py -c 200 404`

Help ?  
`$ python3 urlyze.py --help`

```
optional arguments:
  -h, --help            show this help message and exit
  -i [input file], --input [input file]
                        Input file with URLs, if not provided will read from STDIN
  -o [output file], --output [output file]
                        Writes input in the output file, if not provided will write to STDOUT
  -c [ [ ...]], --status-code [ [ ...]]
                        List of status codes to be written to the output
  -V, --verbose         Allows redirection, shows status code | content length | url | number of redirects
  -t , --timeout        Time out request after n seconds. Default 5 seconds
  -L , --rate-limit     Rate limit your request, each request after n seconds
  --user-agent {chrome,firefox,safari}
                        choose user-agent
  --mobile              flag for user-agent to use mobile user agent string
  -m , --method         HTTP method to be used. GET/HEAD, default: GET
  -r, --redirect        To allow redirects on the URLs. Default: False
  -e, --show-error      show error URLs at the end of output
```

## License

URLyze is licensed under the GNU Affero General Public License version 3 or later. See the accompanying file LICENSE or http://www.gnu.org/licenses/agpl.html.


> ###### Feel free to create pull request, if you have any issues or suggestions.
