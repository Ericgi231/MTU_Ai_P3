'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"
    out = []
    for card in cards:
        out.append([Cluedo.getIdentifierFromNames(hand,card)])
    return out

def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    out = []
    single = []
    for card in Cluedo.cards:
        for hand in Cluedo.hands:
            single.append(Cluedo.getIdentifierFromNames(hand,card))
        out.append(single)
        single = []
    return out

def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    out = []
    single = []
    for card in Cluedo.cards:
        for hand1 in Cluedo.hands:
            for hand2 in Cluedo.hands:
                if hand1 != hand2:
                    single.append(-Cluedo.getIdentifierFromNames(hand1,card))
                    single.append(-Cluedo.getIdentifierFromNames(hand2,card))
                    out.append(single)
                    single = []
    return out

def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    out = []
    single = []
    for card in Cluedo.suspects:
        single.append(Cluedo.getIdentifierFromNames(Cluedo.casefile,card))
    out.append(single)
    single = []

    for card in Cluedo.weapons:
        single.append(Cluedo.getIdentifierFromNames(Cluedo.casefile,card))
    out.append(single)
    single = []

    for card in Cluedo.rooms:
        single.append(Cluedo.getIdentifierFromNames(Cluedo.casefile,card))
    out.append(single)

    return out

def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    out = []
    single = []
    for card1 in Cluedo.suspects:
        for card2 in Cluedo.suspects:
            if card1 != card2:
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card1))
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card2))
                out.append(single)
                single = []

    for card1 in Cluedo.weapons:
        for card2 in Cluedo.weapons:
            if card1 != card2:
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card1))
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card2))
                out.append(single)
                single = []

    for card1 in Cluedo.rooms:
        for card2 in Cluedo.rooms:
            if card1 != card2:
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card1))
                single.append(-Cluedo.getIdentifierFromNames(Cluedo.casefile,card2))
                out.append(single)
                single = []

    return out

def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    #suggester asks for cards 1, 2, 3
    #refuter has 1 of the cards
    #if card shown, we know refuter has that card
    out = []

    if refuter != None: #card was refuted
        start = Cluedo.suspects.index(suggester)
        end = Cluedo.suspects.index(refuter)
        for n in range(start+1, end+1):
            index = n % len(Cluedo.suspects)
            if n == end: #refuter
                if cardShown != None: #card shown
                    out.append([Cluedo.getIdentifierFromNames(Cluedo.suspects[index], cardShown)])
                else: #card not shown
                    out.append([
                        Cluedo.getIdentifierFromNames(Cluedo.suspects[index], card1),
                        Cluedo.getIdentifierFromNames(Cluedo.suspects[index], card2),
                        Cluedo.getIdentifierFromNames(Cluedo.suspects[index], card3)
                    ])
            else: #in between
                out.append([-Cluedo.getIdentifierFromNames(Cluedo.suspects[index],card1)])
                out.append([-Cluedo.getIdentifierFromNames(Cluedo.suspects[index],card2)])
                out.append([-Cluedo.getIdentifierFromNames(Cluedo.suspects[index],card3)])
    else: #card was not refuted
        for player in Cluedo.suspects:
            if player != suggester:
                out.append([-Cluedo.getIdentifierFromNames(player,card1)])
                out.append([-Cluedo.getIdentifierFromNames(player,card2)])
                out.append([-Cluedo.getIdentifierFromNames(player,card3)])

    return out

def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    out = []

    if correct:
        out.append([Cluedo.getIdentifierFromNames(Cluedo.casefile,card1)])
        out.append([Cluedo.getIdentifierFromNames(Cluedo.casefile,card2)])
        out.append([Cluedo.getIdentifierFromNames(Cluedo.casefile,card3)])
    else:
        out.append([-Cluedo.getIdentifierFromNames(accuser,card1)])
        out.append([-Cluedo.getIdentifierFromNames(accuser,card2)])
        out.append([-Cluedo.getIdentifierFromNames(accuser,card3)])
        
        out.append([
            -Cluedo.getIdentifierFromNames(Cluedo.casefile,card1),
            -Cluedo.getIdentifierFromNames(Cluedo.casefile,card2),
            -Cluedo.getIdentifierFromNames(Cluedo.casefile,card3)
        ])

    return out
