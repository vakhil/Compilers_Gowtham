if x > 2
   print "x is greater than 2"
elsif x <= 2 and x!=0
   print "x is 1"
else
   print "I can't guess the number"
end

# Simple for loop using a range.
for i in (1..4)
    print i," "
end
print "\n";

for i in (1...4)
	print i," " + 2
end
print "\n"

# Running through a list (which is what they do).
items = [ "Mar", 12, "goobers", 18.45 ]
for it in items
    print it, " "
end
print "\n"

# Go through the legal subscript values of an array.

