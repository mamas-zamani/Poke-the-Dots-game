def append_fibonacci(integer_list):
  if len(integer_list) < 2:
    integer_list.append(1)
  else:
    integer_list.append(integer_list[len(integer_list)-1] + integer_list[len(integer_list)-2])

def fibonacci(max):
  ans = []
  max = int(max)
  if max == 0:
    return ans
  else:
    ans.append(1)
    ans.append(1)
    while ans[len(ans)-1] + ans[len(ans)-2] <= max:
      append_fibonacci(ans)
  return ans
def main():
  ll = input('Enter a non-negative integer >')
  if(ll.isdigit()):
    res = fibonacci(ll)
    print("The Fibonacci series starts with:",res)
  else:
    print(ll,"is not a non-negative integer")
main()
