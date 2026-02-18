def get_card_score(card):
        RED_KING_DIAMOND = 38
        RED_KING_HEART = 51
        if card >= 52:
            return 0
        #In cambio red kings are minus one so add check here
        if card == RED_KING_DIAMOND or card == RED_KING_HEART:
            #red kings are worth -1
            return -1
        score = card % 13
        score = score + 1
        if score >= 10:
            return 10

        return score

def convert_card(card):
        #check for -2
        if card == -2:
            return "No Card"
        #check for joker
        if card >= 52:
            return "JK"
        #turn the int values into a card
        cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
        #A = 1, JK = joker
        #// MEANS DIVIDE AND FLOOR (FLOOR REMOVES DECIMALS)
        suits = 'SCDH'[card//13]
        return cards + suits

def main():
     for i in range(54):
          print("index: " , i , " is worth: ", get_card_score(i) , " card name is : " , convert_card(i))

main()


    