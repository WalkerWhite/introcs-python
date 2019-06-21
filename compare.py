import sys
import os.path
import difflib
from filecmp import dircmp, cmp


def print_diff_contents(file1,file2):
    source1 = open(file1)
    text1 = source1.read().split('\n')
    source1.close()
    source2 = open(file2)
    text2 = source2.read().split('\n')
    source2.close()
    
    #diff = difflib.Differ().compare(text1,text2)
    diff = difflib.unified_diff(text1, text2, lineterm='')
    print('\n'.join(diff))



def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("Diff found for %s found in %s and %s" % (repr(name), repr(dcmp.left), repr(dcmp.right)))
        print_diff_contents(os.path.join(dcmp.left,name),os.path.join(dcmp.right,name))
    
    for sub in dcmp.subdirs:
        print_diff_files(dcmp.subdirs[sub])

def main():
    if len(sys.argv) != 3:
        print('usage: python compare.py dir1 dir2')
    
    root = os.path.split(__file__)[0]
    file1 = os.path.join(root,sys.argv[1])
    file2 = os.path.join(root,sys.argv[2])
    assert os.path.isdir(file1) == os.path.isdir(file2), '%s and %s are not comparable' % (repr(sys.argv[1]),repr(sys.argv[1]))
    
    if os.path.isdir(file1):
        dcmp = dircmp(file1,file2)
        print_diff_files(dcmp)
    else:
        if not cmp(file1,file2):
            print('Diff found for %s and %s ' % (repr(file1), repr(file2)))
            print_diff_contents(file1,file2)


if __name__ == '__main__':
    main()