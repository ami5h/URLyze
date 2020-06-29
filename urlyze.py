#!/usr/bin/python3
import requests, argparse, sys, time


class InputMissing(Exception): pass

class Urlyze:

	headers = {}

	def __init__(self, args):
		self.args = args
		self.input_list = [i.strip() for i in args.input.readlines()]
		self.output = args.output
		self.status_code = list(set(args.status_code)) if args.status_code else None
		self.session = requests.session()
		self.errors = {"total":0, "urls":[]}

	def set_useragent(self, ua):
		user_agents = {
		"chrome":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
		"firefox":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
		"safari":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"mchrome":"Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
		"mfirefox":"Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0",
		"msafari":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"		
		}
		ua = ua if not self.args.mobile else f"m{ua}"
		Urlyze.headers['User-Agent'] = user_agents[ua]

	def catch_errors(func):
		def wrapper(self, *args):
			try: 
				res = func(self, *args)
			except requests.exceptions.RequestException as e:
				self.errors['total'] += 1
				self.errors['urls'].append(f"[Error]\t{args[0]}")
				res = None
			return res
		return wrapper	

	def rate_limit(func):
		def wrap(self, *args):
			sec = self.args.rate_limit
			if sec:
				time.sleep(sec)
			res = func(self, *args)
			return res
		return wrap

	@catch_errors
	@rate_limit
	def make_request(self, url):
		res = self.session.request(self.args.method, url, headers=Urlyze.headers, allow_redirects=(self.args.redirect or self.args.verbose),
									timeout=self.args.timeout )
		return res

	def parse_input(self):
		for url in self.input_list:
			res = self.make_request(url)
			if not res:
				continue
			self.print_response(res)

	def print_response(self, r):
		if not self.args.status_code:
			self.output.write(f"{self.to_str(r, self.args.verbose)}\n")
		else:
			if str(r.status_code) in self.status_code:
				self.output.write(f"{self.to_str(r, self.args.verbose)}\n")
			else: return
		

	def to_str(self, r, is_verbose):
		if is_verbose:
			try:
				c_l = r.headers['Content-Length']
			except KeyError:
				c_l = -1
			return f"{r.status_code}\t{c_l}\t{r.history[0].request.url if len(r.history)>0 else r.request.url}\t{len(r.history)}"
		else:
			return f"{r.status_code}\t{r.request.url}"



def main():
	args = read_args()
	urls = Urlyze(args)
	if args.user_agent: 
		urls.set_useragent(args.user_agent)
	print("[+] Output will be written in the given file" if not args.output == sys.stdout else "[+] URLyze - URL Analyzer")
	try:
		urls.parse_input()
	except KeyboardInterrupt:
		print("Bye!!")
	print(f"Total URL errors: {urls.errors['total']}")
	if args.show_error:
		for url in urls.errors['urls']:
			args.output.write(f"{url}\n")

def read_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", metavar='input file', type=argparse.FileType('r', encoding="utf-8"), nargs='?', default=(None if sys.stdin.isatty() else sys.stdin), 
																help="Input file with URLs, if not provided will read from STDIN")
	parser.add_argument("-o" , "--output", metavar='output file', type=argparse.FileType('w', encoding="utf-8"), nargs='?', default=sys.stdout,
																help="Writes input in the output file, if not provided will write to STDOUT")
	parser.add_argument("-c", "--status-code", nargs='*', metavar='', default=None, help="List of status codes to be written to the output")
	parser.add_argument("-V", "--verbose", action="store_true", help="Allows redirection, shows status code | content length | url | number of redirects")
	parser.add_argument("-t", "--timeout", metavar='', type=int, choices=range(0, 31), default=5, help="Time out request after n seconds. Default 5 seconds")
	parser.add_argument("-L", "--rate-limit", metavar='', type=int, choices=range(0, 61), default=None, help="Rate limit your request, each request after n seconds")
	parser.add_argument("--user-agent", type=str.lower, choices=["chrome", "firefox", "safari"], default=None, help="choose user-agent")
	parser.add_argument("--mobile", action="store_true", help="flag for user-agent to use mobile user agent string")
	parser.add_argument("-m", "--method", type=str.upper, metavar='', choices=["GET", "HEAD"], default="GET", help="HTTP method to be used. GET/HEAD, default: GET")
	parser.add_argument("-r", "--redirect", action="store_true", help="To allow redirects on the URLs. Default: False")
	parser.add_argument("-e", "--show-error", action="store_true", help="show error URLs at the end of output")
	args = parser.parse_args()
	if len(sys.argv)==1 and not args.input:
		parser.print_help()
		exit()
	return args

if __name__ == '__main__':
	main()
