"""
TASK

Mark and Jane are very happy after having their first child. Their son loves toys, so Mark wants to buy some. There are a number of different toys lying in front of him, tagged with their prices. Mark has only a certain amount to spend, and he wants to maximize the number of toys he buys with this money. Given a list of toy prices and an amount to spend, determine the maximum number of gifts he can buy.
Each toy can be purchased only once.

Example
prices = 1,2,3,4 k = 7

The budget is 7 units of currency. He can buy items that cost 1,2,3 for 6 , or 3,4 for 7 units. The maximum is 3 items.

Function Description
Complete the function maximumToys in the editor below.

Input maximumToys has the following parameter(s):

int pricesn: the toy prices
int k: Mark's budget
Returns

int: the maximum number of toys
Input Format
The first line contains two integers, and , the number of priced toys and the amount Mark has to spend. The next line contains space-separated integers

A toy can't be bought multiple times.

Sample Input
7 50 1 12 5 111 200 1000 10

Sample Output
4

Explanation
He can buy only toys at most. These toys have the following prices: 1,12,5,10.
"""

def max_toys(prices, k):
    '''
    prices: list
    k: int
    '''
    count = 0
    sum = 0
    prices.sort()
    for i in prices_list:
        sum += i
        if sum > k:
            break
        else:
            count += 1
    
    return count

if __name__ == '__main__':
    number_toys = int(input('Enter number of toys:'))
    k = int(input('Enter your budget:'))
    prices_list = []
    for i in range(number_toys):
        prices_list.append(int(input('Enter toy price:')))

    number_toys = max_toys(prices_list, k)
    print(f'Mark and Jane can buy a maximun of {number_toys} toys.')