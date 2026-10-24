
def merge(self, nums1, m, nums2, n):
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
        return nums1.sort()

            