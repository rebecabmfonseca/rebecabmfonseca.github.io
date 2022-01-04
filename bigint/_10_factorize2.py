#!/usr/bin/env python
# coding: UTF-8
#
## @package _10_factorize2
#
#   A faster factorization algorithm.
#
#   The fundamental theorem of arithmetic states that every positive integer
#   (except the number 1) can be represented in exactly one way, apart from
#   rearrangement, as a product of one or more primes
#   (Hardy and Wright 1979, pp 2-3).
#   <p>
#   This is a "fast" algorithm, which can factorize large numbers in a
#   reasonably small time.
#
#   @author Paulo Roma
#   @since 27/12/2008
#   @see http://mathworld.wolfram.com/PrimeFactorizationAlgorithms.html
#   @see http://www.nationmaster.com/encyclopedia/Prime-factorization-algorithm
#   @see http://en.wikipedia.org/wiki/User:Ohanian

from __future__ import print_function

import sys

from _04b_intsqrt import intsqrt
from _04d_sieve import sieve
try:
    from HTMLParser import HTMLParser   # Python 2.6-2.7
    input = raw_input
except ImportError:
    import html                         # Python 3

## a list with the first 10 primes
ListOfPrimes = sieve(10)
## length of ListOfPrimes
maxindex = len(ListOfPrimes)
## the last prime in the ListOfPrimes
maxprimeinlist = ListOfPrimes[-1]

try:
    ## translation table for creating superscript.
    superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    ## translation table for creating subscript.
    subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
except:
    superscript = {ord(c): ord(t)
                   for c, t in zip(u"0123456789", u"⁰¹²³⁴⁵⁶⁷⁸⁹")}
    subscript = {ord(c): ord(t) for c, t in zip(u"0123456789", u"₀₁₂₃₄₅₆₇₈₉")}

##
#   @brief Checks if a given integer is prime
#
#   @param n given integer.
#   @return True if n is a prime, and false otherwise.
#
def isPrime(n):
    global ListOfPrimes
    high = intsqrt(n)
    for x in ListOfPrimes:
        if x <= high and n % x == 0:
            return False
        if x >= high:
            return True

    x = maxprimeinlist + 2
    while x <= high:
        if n % x == 0:
            return False
        x += 2
    return True

##
#   @brief Factorizes an integer or long number.
#
#   @param n given integer.
#   @return a list with the prime factors of n.
#
def factorize(n):
    primes = []
    index = 0
    candidate = ListOfPrimes[index]
    # long operations take too much time
    if (n < sys.maxsize):
        n = int(n)
    if isPrime(n):
        primes = [n]
        return primes
    while candidate < intsqrt(n) + 1:
        if n % candidate == 0:
            # All factors of "n", lesser than "candidate", have been found before.
            # Therefore, "candidate" cannot be composite.
            n = n // candidate
            primes += [candidate] + factorize(n)
            break
        index += 1
        if index < maxindex:
            candidate = ListOfPrimes[index]
        else:
            candidate += 2
    return primes


## Return a superscript string for the given value.
#
#  @param val a numeric string.
#  @param type select the superscript method.
#  @return a new superscript string.
#
def exponent(val, type=False):
    if type:
        return "<sup>{}</sup>".format(val)
    elif superscript is not None:
        if isinstance(val, bytes):
            val = unicode(val, 'utf-8')
        return val.translate(superscript)
    else:
        return "^{}".format(val)

##
#   @brief Condenses the list of prime factors of a number,
#   so that each factor appears just once, in the format @f$prime^{nth_{power}}@f$.
#
#   e.g., python factorize2.py 173248246132375748867198458668657948626531982421875 <br>
#   - ['3²⁴', '5¹⁴', '7³³', '13'] (unicode translation table)
#   - ['3^24', '5^14', '7^33', '13'] (None)
#
#   @param L a list with the prime factors of a number.
#   @return a condensed list.
#
def condense(L):
    prime, count, list = None, None, []
    for x in L:
        if x == prime:
            count += 1
        else:
            if prime:
                list += [str(prime)]
                if (count > 1):
                    list[-1] += exponent(str(count))
            prime, count = x, 1
    list += [str(prime)]
    if (count > 1):
        list[-1] += exponent(str(count))
    return list

## Stringify a condensed list of factors.
#
#  Each factor is separated by a ''&times;'' symbol:
#
#  345
#  - 3 × 5 × 23
#
#  173248246132375748867198458668657948626531982421875
#  - 3²⁴ × 5¹⁴ × 7³³ × 13
#
#  @param lfactor list of factors.
#  @return string of factors.
#
def toString(lfactor):
    st = ""
    for i, f in enumerate(lfactor):   # it can be a long or int
        try:
            st += "%s %s " % (f, "" if i == len(lfactor) -
                              1 else HTMLParser().unescape('&times;'))
        except:
            st += "{} {} ".format(f, "" if i == len(lfactor) -
                                  1 else html.unescape('&times;'))
    return st

##
#   @brief main function for testing.
#
#   argv:
#   - argv[0]: path.
#   - argv[1]: integer to be factorized.
#
#   Usage:
#   - _10_factorize2.py 345
#
def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        n = input("An integer argument is needed: ")
        argv.append(n)

    if not argv[1].isdigit():
        print("A positive integer is expected.")
        return 1

    import time
    t0 = time.time()
    print(toString(condense(factorize(eval(argv[1])))))
    print("\nRun time: %gs" % (time.time() - t0))

    sys.argv[1] = input("\nEnter next number to be factorized: ")
    main()

    return 0


try:
    if __name__ == '__main__':
        sys.exit(main())
except (KeyboardInterrupt, EOFError):   # used Ctrl-c to abort the program
    print("Bye, bye... See you later alligator.")
except OSError as msg:
    print(msg)
