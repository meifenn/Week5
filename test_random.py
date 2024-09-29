import random
from utility import MarbleBag 
from utility import Success
from utility import Progressive


# random.seed(10)
# for i in range(10):
    # print(int(random.uniform(0,10)))
    # print(random.choices([1,2,3,4]))

#Main---------------------------------------------------
def main():
    
    pro=Progressive(10,10)
    for _ in range(10):
        # Success.attempt(20)
        pro.attempt()
    # original_bag=MarbleBag(['blue','red','black','gold'])

    # for i in range(10):
    #     print(original_bag.draw())

if __name__=='__main__':
    main()