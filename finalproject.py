import simplegui
import random

#global variences
WIDTH = 800
HEIGHT = 500
card_WIDTH = 40
card_HEIGHT = 1.6 * card_WIDTH
NUMBER_SIZE = 0.8 * card_WIDTH
DECK_POS = [640,80]
player_numbers = 2

class Message:
    def __init__(self, pos,information = ''):
        self.information = information
        self.pos = pos
        
    def change_information(self, information):
        self.information = information
        
    def change_pos(self, pos):
        self.pos = pos
        
    def draw(self, canvas):
        canvas.draw_text(self.information, self.pos , 20, 'Black')
    
class Card:
    def __init__(self, color, number, pos, exposed = False):
        if color == 'White':
            self.color = 1
        else:
            self.color = 0
        self.number = number
        self.rank = self.number * 2 + self.color
        self.pos = list(pos)		#position listed above the cards
        self.exposed = exposed		#if the position is visible
        
    def get_rank(self):
        return self.rank
    
    def get_color(self):
        return self.color
        
    def get_pos(self):
        return self.pos
    
    def change_pos(self, new_pos):
        self.pos = list(new_pos)
    
    def expose(self):
        self.exposed = True
        known_list.append(self.rank)
        if self.rank in unknown_list:
            unknown_list.remove(self.rank)
        
    def __str__(self):
        return 'card number: '+str(self.number)+' card rank : '+str(self.rank)
    
    #check if the card is chosen or not
    def is_chosen(self, point):
        return (self.pos[0]< point[0] < self.pos[0]+card_WIDTH)and(
            self.pos[1] < point[1] < self.pos[1]+card_HEIGHT)
                
    
    def draw(self,canvas):
        #draw the white card
        canvas.draw_line((self.pos[0]+0.5*card_WIDTH,self.pos[1]-5),
                         (self.pos[0]+0.5*card_WIDTH,self.pos[1]+card_HEIGHT+5),card_WIDTH+10,'Navy')
        if self.color:
            if self.exposed:
                canvas.draw_line((self.pos[0]+0.5*card_WIDTH,self.pos[1]),
                                 (self.pos[0]+0.5*card_WIDTH,self.pos[1]+card_HEIGHT),card_WIDTH,'White')
                canvas.draw_text(str(self.number),
                                 (self.pos[0]+0.5*card_WIDTH-0.5*NUMBER_SIZE,self.pos[1]+0.5*card_HEIGHT+0.5*NUMBER_SIZE),
                                 NUMBER_SIZE,'Black')
            else:
                canvas.draw_line((self.pos[0]+0.5*card_WIDTH,self.pos[1]),
                                 (self.pos[0]+0.5*card_WIDTH,self.pos[1]+card_HEIGHT),card_WIDTH,'WHITE')
        #draw the black card
        else:
            if self.exposed:
                canvas.draw_line((self.pos[0]+0.5*card_WIDTH,self.pos[1]),
                                 (self.pos[0]+0.5*card_WIDTH,self.pos[1]+card_HEIGHT),card_WIDTH,'Black')
                canvas.draw_text(str(self.number),
                                 (self.pos[0]+0.5*card_WIDTH-0.5*NUMBER_SIZE,self.pos[1]+0.5*card_HEIGHT+0.5*NUMBER_SIZE),
                                 NUMBER_SIZE,'White')
            else:
                canvas.draw_line((self.pos[0]+0.5*card_WIDTH,self.pos[1]),
                                 (self.pos[0]+0.5*card_WIDTH,self.pos[1]+card_HEIGHT),card_WIDTH,'Black')
            
         
class Player:
    def __init__(self, order, pos, cards = []):
        self.order = order
        self.cards = list(cards)
        self.pos = list(pos)
        self.out = False		#check if the player is out
        self.human = False
        self.next_p = None
        
    def change_human_label(self):
        self.human = True
        
    def get_order(self):
        return self.order
    
    def change_order(self,new_order):
        self.order = new_order
    
    #deal a card
    def deal(self,my_deck):
        card = my_deck.pop()    
        self.cards.append(card)
        card.change_pos((self.pos[0]+len(self.cards)*card_WIDTH,self.pos[1]))
        return card
        
    #sort the cards
    def sort(self):
        self.cards = list(sorted(self.cards, key = lambda card:card.rank))
        for card in self.cards:
            card.change_pos((self.pos[0]+self.cards.index(card)*card_WIDTH,self.pos[1]))
        return self.cards
   
    def exposed_cards(self):
        return [card for card in self.cards if card.exposed]
    
    #heuristic predict algorithm
    def predict(self, player, index):
        chosen_card = player.cards[index]
                
        my_known_list = []
        for card in self.cards:
            my_known_list.extend([card.get_rank()])
        my_known_list.extend(known_list)
        guess_list = [rank for rank in unknown_list if not(rank in my_known_list)]
        
        guess_list = [i for i in list(guess_list) if i%2 == chosen_card.get_color()]
        
        n = len(player.cards)
        m = n - index
        guess_list = [i for i in list(guess_list) if i >= index and i <= 23-m+1]
        
        lower_bound = -1
        upper_bound = -1
        c_up = 0			
        c_low = 0
        for card in player.cards[index+1:]:
            if card.exposed:
                upper_bound = card.get_rank()
                break
            if card.get_color() == chosen_card.get_color():
                c_up += 1
                
        for i in range(index-1,-1,-1):
            if player.cards[:index][i].exposed:
                lower_bound = player.cards[:index][i].get_rank()
                break
            if card.get_color() == chosen_card.get_color():
                c_low += 1
        
        if upper_bound > -1:
            guess_list = [i for i in list(guess_list) if i < upper_bound]
        if lower_bound > -1:
            guess_list = [i for i in list(guess_list) if i > lower_bound]
        
        if upper_bound == -1:
            upper_bound = 22
        if lower_bound == -1:
            lower_bound = 0
        guess_list = [i for i in list(guess_list) if 
                      (i//2 <= upper_bound//2 - c_up and i//2 >= lower_bound//2 +c_low)]
        
        p = 1.0 / len(guess_list)
        result = [random.choice(guess_list) // 2, p]       
        return result
    
    #the baseline solver predict algoeithm
    def silly_predict(self, player, index):
        chosen_card = player.cards[index]
                
        my_known_list = []
        for card in self.cards:
            my_known_list.extend([card.get_rank()])
        my_known_list.extend(known_list)
        guess_list = [rank for rank in unknown_list if not(rank in my_known_list)]
        
        
        p = 1.0 / len(guess_list)
        result = [random.choice(guess_list) // 2, p]
        return result
        
    def draw(self, canvas):
        for card in self.cards:
            card.draw(canvas)
            
    def draw_number(self, canvas):
        for card in self.cards:
            canvas.draw_text(str(card.number),
                             (card.get_pos()[0],card.get_pos()[1]-10),15,'Black')
    
#helper functions
def new_game():
    global deck, chosen_mark, chosen_card, players, player_alive_numbers
    global known_list, unknown_list, can_deal, can_guess, process_flag
    global inturn_message, guess_message, hint_message
    global player_inturn
    hint_message = Message((400,30))
    inturn_message = Message((10,80), 'In Turn ')
    guess_message = Message((20,120))
    unknown_list = range(24)
    known_list = []
    chosen_mark = ()
    chosen_card = []
    process_flag = 1
    players = range(player_numbers)
    player_alive_numbers = player_numbers
    
    #stop the timer
    if timer1.is_running:
        timer1.stop()
    
    can_deal = [True, True]
    can_guess = [True, True]
    
    deck = []
    for i in range(12):
        card = Card('Black', i, DECK_POS)
        deck.append(card)
        card = Card('White', i, DECK_POS)
        deck.append(card)
    random.shuffle(deck)#shuffle all cards
    for i in range(len(deck)):
        deck[i].change_pos((DECK_POS[0]+i*8,DECK_POS[1]))
    
    random_order = random.randrange(player_numbers+1)
    for i in range(player_numbers):
        order = (random_order + i) % player_numbers
        players[i] = Player(order, [100, order * (card_HEIGHT + 50) + 30])
    for i in range(player_numbers):
        players[i].next_p = players[(i+1)%player_numbers]
        
    players[0].change_human_label()
    
    first_player = (player_numbers-players[0].get_order())%(player_numbers)
    player_inturn = players[first_player]
    
    for player in players:
    #draw three cards at the beginning of the game
        for i in range(3):       
            player.deal(deck)  
        player.sort()    
    
    #start the game        
    hint_message.change_information('Game Start!')
    timer1.start()
   
#judge if the baseline solver guesses it right
def judge1(guess, player):
    if not chosen_card:
        hint_message.change_information("No card is selected")
    elif not(chosen_card in player.cards):
        hint_message.change_information("Invalid chosen card")
    elif can_guess[0] and can_guess[1]:
        guess_message.change_information('Guess: '+str(player.cards.index(chosen_card))+' to be '+str(guess))
        guess_message.change_pos((player.pos[0],player.pos[1]+card_HEIGHT+25))
        if guess == chosen_card.number :#if the guess is right
            chosen_card.expose()
            hint_message.change_information(' Right!')		
        else:
            new_card.expose()
            hint_message.change_information(' Wrong!')
        can_guess[0] = False 
        can_guess[1] = False
        can_deal[1] = True
        #print unknown_list
        out_process(player)
        timer1.start()    
        

#judge if the heuristic solver guesses it right   
def judge2(guess, player):
    if chosen_card:
        guess_message.change_information('Guess: '+str(player.cards.index(chosen_card))+'to be '+str(guess))
        guess_message.change_pos((player.pos[0],player.pos[1]+card_HEIGHT+25))
        if guess == chosen_card.number :#if the guess is right
            chosen_card.expose()
            hint_message.change_information(' Right!')		
        else:
            new_card.expose()
            hint_message.change_information(' Wrong!')
        can_guess[0] = False
        can_guess[1] = True
        out_process(player)
    print unknown_list
        
#check and deal if any player is out
def out_process(player):
    global player_alive_numbers, player_inturn
    hidden_cards = [card for card in player.cards if not card in player.exposed_cards()]
    if hidden_cards == []:
        player.out = True
    record = player_inturn
    player_inturn = player_inturn.next_p 
    
    for i in range(player_numbers):
        if players[i].out: 
            if i == 0:
                hint_message.change_information('You lose!')
                timer2.start()
            elif players[i].get_order() < player_alive_numbers:	
                hint_message.change_information('player '+ str(i+1)+' Out.')
                print "when out: " + str(record.get_order())
                player_inturn = record
                player_inturn.next_p = player_inturn.next_p.next_p
                if player_inturn.human:
                    deal_handler()
                    can_guess[1] = True
                    print "next: "+str(player_inturn.next_p.get_order())
                
                player_alive_numbers -= 1
                if player_alive_numbers == 1:
                    hint_message.change_information('You Win!')
                    timer2.start()
                print 'player_alive_numbers: '+str(player_alive_numbers)
                if players[i].get_order() != player_alive_numbers:	
                    for t in range((i+1)%(player_alive_numbers+1),player_alive_numbers+1):
                        temp = (players[t%player_alive_numbers].get_order()-1)%player_alive_numbers
                        players[t%player_alive_numbers].change_order(temp)
                        print 'player ' + str(t)+', order: '+str(players[t%player_alive_numbers].get_order())
                    players[i].change_order(player_alive_numbers+1)
                
    
#the heuristic solver draws and guesses cards 
def process(player1,player2):
    global chosen_card, new_card, chosen_mark
    inturn_message.change_pos((player1.pos[0]-90,player1.pos[1]+card_HEIGHT*0.5))
    #draw cards   
    if len(deck)>1 and can_deal[1]:
        new_card = player1.deal(deck)
    player1.sort()    
    if can_deal[1]:
        hidden_cards = [card for card in player2.cards if not card in player2.exposed_cards()]
        if hidden_cards:          
            #make a guess depends on the maximum probability
            max_p = [0,0]
            for card in hidden_cards:
                chosen_index = player2.cards.index(card)
                result = player1.predict(player2,chosen_index)
                if result[1] > max_p[1]:
                    max_p = list(result)
                    chosen_card = card
                    
            chosen_mark = (chosen_card.get_pos()[0]+10,chosen_card.get_pos()[1]-10)
            guess = max_p[0]
            judge2(guess,player2)      
        else:
            player2.out = True
            hint_message.change_information('Error: no card to be guess.')
        
#the baseline solver draws and guesses cards
def silly_process(player1,player2):
    global chosen_card, new_card, chosen_mark
    inturn_message.change_pos((player1.pos[0]-90,player1.pos[1]+card_HEIGHT*0.5))
    #draw cards
    if len(deck)>1 and can_deal[1]:
        new_card = player1.deal(deck)
    player1.sort()    
    if can_deal[1]:
        hidden_cards = [card for card in player2.cards if not card in player2.exposed_cards()]
        if hidden_cards:          
            max_p = [0,0]
            for card in hidden_cards:
                chosen_index = player2.cards.index(card)
                result = player1.silly_predict(player2,chosen_index)
                max_p = list(result)
                chosen_card = card
                    
            chosen_mark = (chosen_card.get_pos()[0]+10,chosen_card.get_pos()[1]-10)
            guess = max_p[0]
            judge2(guess,player2)      
        else:
            player2.out = True
            hint_message.change_information('Error: no card to be guess.')
           
def deal(color):
    global new_card
    
    random.shuffle(deck)
    for i in range(len(deck)):
        deck[i].change_pos((DECK_POS[0]+i*8,DECK_POS[1]))
          
    temp_deck = [card for card in deck if card.get_color() == color]
    if len(temp_deck) == 0:
        temp_deck =[card for card in deck if card.get_color() == (1 - color)]
    
    if len(deck)>1 and temp_deck and can_deal[0]:
        new_card = players[0].deal(temp_deck)
        deck.remove(new_card)
    players[0].sort()
    can_deal[0] = True
    can_guess[0] = True
    hint_message.change_information('Please guess')
    
def draw(canvas):
    hint_message.draw(canvas)
    inturn_message.draw(canvas)
    guess_message.draw(canvas)
    if chosen_mark:
        canvas.draw_circle(chosen_mark,5,10,'Red')
    for card in deck:
        card.draw(canvas)
    for player in players:
        player.draw(canvas)
    players[0].draw_number(canvas)
    
 
#define handlers
def click(pos):
    global chosen_card, chosen_mark
    for card in players[0].next_p.cards:
        if card.is_chosen(pos):
            chosen_mark = (card.get_pos()[0]+10,card.get_pos()[1]-10)
            chosen_card = card 
            #print card
            
def newgame_handler():
    new_game()
    
def deal_handler():
    deal(random.choice([0,1]))

def deal_white_handler():
    deal(1)
    
def deal_black_handler():
    deal(0)
    
def input_handler(input_text):
    guess = int(input_text)
    judge1(guess,players[0].next_p)    
    
def input_number_handler(number):
    global player_numbers
    player_numbers = int(number)

def time_handler1():
    global player_inturn
    timer1.stop()
    
    #the baseline solver's turn
    if player_inturn.human:
        silly_process(player_inturn,player_inturn.next_p)
        timer1.start()
    #the heuristic solver's turn
    else:
        process(player_inturn,player_inturn.next_p)
        timer1.start()    
    
#when the game ends
def time_handler2():
    new_game()
    timer2.stop()
    
#initialize frame
frame = simplegui.create_frame("Da Vinci Code", WIDTH, HEIGHT)

#register handlers
timer1 = simplegui.create_timer(2000,time_handler1)
timer2 = simplegui.create_timer(3000,time_handler2)
frame.set_draw_handler(draw)
frame.set_canvas_background('#FFDAB9')
frame.set_mouseclick_handler(click)
frame.add_button('New game',newgame_handler,150)
frame.add_input('Number of players',input_number_handler,150)
frame.add_button('Deal randomly',deal_handler,150)
frame.add_button('deal white',deal_white_handler,80)
frame.add_button('deal black',deal_black_handler,80)
frame.add_input('My guess',input_handler,150)
frame.add_button('deal white',deal_white_handler,80)

frame.start()

#start a new game
new_game()
        
        