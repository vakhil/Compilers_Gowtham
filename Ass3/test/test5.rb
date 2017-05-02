require("good")

#Lats code in the modules

masch = Addition.parse('+')
    assert(masch)
    assert(masch.matches)
    assert_equal(2, masch.matcheslength)

