s = "Hi t here.  How are you?"
print s.length, " [" + s + "]\n"
s[1] = 12.33
# Selecting a character in a string gives an integer ascii code.
print s[4], "\n"
#printf("%c\n", s[4])

# The [n,l] substring gives the starting position and length.  The [n..m]
# form gives a range of positions, inclusive.

print "[" + s[4.4,4] + "] [" + s[6..15] + "]\n"
print "Wow " * 3, "\n"

print s.index, " ", s.length, " ", s.index, "\n"

print s.reverse, "\n"


