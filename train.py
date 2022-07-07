# File contating all the function which is used in main file for traing the ai

# def calculate_fitness(g1,g2,d,lh,rh):

#     g1.fitness += lh*1.5 + d
#     g2.fitness += rh*1.5 + d

# def eval_genemo(genemos, config):
#     global GEN
#     GEN += 1
#     for i,(_,genemo1) in enumerate(genemos):
#         genemo1.fitness = 0
#         for _,genemo2 in genemos[min(i+1,len(genemos)-1):]:
#             genemo2.fitness = 0 if genemo2.fitness == None else genemo2.fitness
#             main(genemo1,genemo2,config,GEN)

# def run_config(config_path):
#     config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

#     # creating population
#     p = neat.Population(config)

#     # adding stat reporters
#     p.add_reporter(neat.StdOutReporter(True))
#     p.add_reporter(neat.StatisticsReporter())

#     # final trained ai will we stored in winner.
#     # winner = p.run(eval_genemo,30)

#     # saving the winner
#     with open('BEST-PADDLE.bin','rb') as file:
#         winner = pickle.load(file)
#         main(winner, config, 0)


# code for handdling AI Movement
# If the paddle move out the screen the move will return false as it is not valid move
# Handling lefts movement

# valid = True
# if left_output.index(max(left_output))  == 0:
#     valid = Left_paddle.move(up = False)
# elif left_output.index(max(left_output))  == 1:
#     g1.fitness -= 0.01
# elif left_output.index(max(left_output))  == 2:
#     valid = Left_paddle.move(up = True)
# if valid == False:
#     g1.fitness -= 1

# handling rights movement
# valid = True
# if right_output.index(max(right_output))  == 0:
#     valid = Right_paddle.move(up = False)
# elif right_output.index(max(right_output))  == 1:
#     g2.fitness -= 0.01
# elif right_output.index(max(right_output))  == 2:
#     valid = Right_paddle.move(up = True)
# if valid == False:
#     g2.fitness -= 1