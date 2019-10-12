#!/usr/bin/env python
import sys
import random
import re

def main():
	originFile = open(sys.argv[1], mode='r')
	outputFile = open('../test_data/npu_trace_output.txt', mode='w+')
	vpp = False; npu = False; jpu = False; vpu = 0; preTs = 0;
	pattern = re.compile(r'^(\s*.*)\s+(\d+\.\d+):\s+.*$')
	for line in originFile:
		m = pattern.match(line)
		if m is None:
			outputFile.write(line)
			continue
		ts = float(m.group(2))
		if preTs == 0:
			preTs = ts
		if ts - preTs < 0.000003:
			outputFile.write(line)
			continue
		nextTs = (ts + preTs) / 2
		ran = random.randint(0, 8)
		if ran == 0:
			ran = random.randint(0, 2)
			outputFile.write('%s %.6f: vpp: %s%s\n' % (m.group(1), nextTs, '+' if not vpp else '-', ['s', 'c', 'r'][ran]))
			vpp = not vpp
		elif ran == 1:
			outputFile.write('%s %.6f: npu: %s\n' % (m.group(1), nextTs, '+' if not npu else '-'))
			npu = not npu
		elif ran == 2:
			outputFile.write('%s %.6f: jpu: %s\n' % (m.group(1), nextTs, '+' if not jpu else '-'))
			jpu = not jpu
		elif ran == 3:
			if random.randint(0, 1) == 0:
				vpu -= 1
			else:
				vpu += 1
			if vpu < 0:
				vpu = 0
			else:
				outputFile.write('%s %.6f: vpu: =%d\n' % (m.group(1), nextTs, vpu))

		outputFile.write(line)
		preTs = ts


main()