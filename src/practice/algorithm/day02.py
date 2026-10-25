
def merge(nums1, m, nums2, n):
    """
    :type nums1: List[int]
    :type m: int
    :type nums2: List[int]
    :type n: int
    :rtype: None Do not return anything, modify nums1 in-place instead.
    """
    #写循环根据m将nums1的m个数遍历出来，根据n将nums2中的n个数遍历出来
    #我觉得还可以通过n将m中的数字遍历出来
    if n==0 and m!=0:
        return nums1
    if m==0 and n!=0:
        nums1[:]=nums2
        return nums1
    if m==0 and n==0:
        return nums1
    for i in range(n):
        nums1[-(i+1)] = nums2[i]
    nums1.sort()
    return nums1
if __name__ == '__main__':
    nums1 = [1,2,3,0,0,0]
    m = 3
    nums2 = [2,5,6]
    n = 3
    print(merge(nums1, m, nums2, n))
    nums1=[0]
    m=0
    nums2=[1]
    n=1
    print(merge(nums1, m, nums2, n))
    nums1=[1]
    m=1
    nums2=[0]
    n=0
    print(merge(nums1, m, nums2, n))

            