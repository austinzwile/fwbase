import argparse
import binaryninja as bn
import os

from rich.console import Console
from rich.panel import Panel

def find_base_address(firmware, verbose):
	print(f"Finding base address for firmware blob: {firmware}.")

	bn.disable_default_log()

	base = bn.BaseAddressDetection(firmware)
	base.detect_base_address()

	base_addr_str = f"Preferred base address @ {hex(base.preferred_base_address)}"

	Console().print(Panel(base_addr_str, width=len(base_addr_str) + 4))

	if verbose:
		for addr, score in base.scores:
			print(f"{hex(addr)} -> {score}")

		for reason in base.get_reasons(base.preferred_base_address):
			print(f"{hex(reason.pointer)} -> {hex(reason.offset)} (type={reason.type})")

def main():
	parser = argparse.ArgumentParser(
		description='Tool to find the base address of firmware',
	)

	parser.add_argument('firmware', type=str, help='Path to the firmware blob')
	parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

	args = parser.parse_args()

	if not os.path.exists(args.firmware):
		print(f"Error: The file '{args.firmware}' does not exist.")
		parser.print_help()
		exit(0)

	find_base_address(args.firmware, args.verbose)

if __name__ == "__main__":
	main()
