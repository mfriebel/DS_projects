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