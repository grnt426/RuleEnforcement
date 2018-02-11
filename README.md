Rule Enforcer
=============

The goal of this enforcer is to allow for the first step in verification that all
rules (or software requirements) are referenced at least once in code. This is 
especially useful for board games, where the rules are explicitly and completely
laid out, and are still brief enough so as to be reasonably capturable
in a single document.

_Note: This is not meant as a substitute for unit tests or integration tests, but
as a complementary tool for tests._

Given a list of rules and a scan directory it will search for references in the code
to determine if a given rule is enforced. Marking a rule as enforced is easy:

```java
// @r1.6
```

The `@r` is the keyword to search on, and all consecutive/decimal separated numbers
are the number of the rule.

The actual rules file is just a new-line separated list of the rules. For example:

```text
7.3. Bidding For Plant
  7.3.1. Turn Order is Clockwise Starting From Auction Leader; Current Player is Bidder
  7.3.2. Bidder Chooses:
    7.3.2.1. Pass, Skip to Rule 7.3.3
    7.3.2.2. Bid at Least 1 Higher on Plant
      7.3.2.2.1. Player Must Pass if They Own Less Money Than Lowest Allowable Bid
  7.3.3. Repeat Rule 7.3.2 Until Only One Bidder Has Not Passed
  7.3.4. Remaining Player Pays Last Bid Price
```

The above format is an example formatting. The rules parser is only looking for the first
example of period separated numbers on a line ending with a period, all else is ignored.

This means an author is free to write whatever comments they want, reference other rules,
nest freely (or not!), skip lines, or list rules out-of-order.

How to Run
----------

```bash
python enforcer.py (rules.txt) (scan directory) [excludepath, excludepath2, ...]
```

What's Next?
-----------

Checking that a referenced rule exists both in code, and in a unit or
integration test, thereby raising the confidence that a given requiurement
is actually met.

Where is This Used?
--------------------

My implementation of PowerGrid relies on this project: https://github.com/grnt426/PowuhGred

The rules are kept here:  https://github.com/grnt426/PowuhGred/blob/master/data/rules.txt

Why Not Some Existing Tool?
-------------------------------------
I was hoping for something simple and light to quickly verify I hadn't forgotten a rule in
building PowerGrid. The board game has quite a few details, exceptions, and
easily forgettable rules that need to be in the game. I could have searched for
'software requirements verification' tools, but didn't want to spend the time evaluating
various solutions, adapting my workflow to them, and then locking myself into whatever
features that software had.

Most importantly, I didn't want some glorified enterprise/corporate solution. I figured I
would be able to create this set of Python scripts to do the bare minimum
of features fairly quickly to keep working on PowerGrid. A couple hours later, and
I have exactly that :)