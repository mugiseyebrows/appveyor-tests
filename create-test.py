from genericpath import isdir
import os
import argparse

def makedirs(path):
    try:
        os.makedirs(path)
    except:
        pass

parser = argparse.ArgumentParser()
parser.add_argument('name')

args = parser.parse_args()

name = args.name

base = os.path.dirname(__file__)

name_ = name.lower()

test_dir = os.path.join(base, 'tests', name_)

makedirs(test_dir)

pro_path = os.path.join(test_dir, name_ + '.pro')

class_name = 'Test' + name
header = '{}.h'.format(class_name.lower())
cpp = '{}.cpp'.format(class_name.lower())

with open(pro_path, 'w', encoding='utf-8') as f:
    f.write("""QT += testlib
SOURCES += main.cpp {}
HEADERS += {}
    """.format(cpp, header))

header_path = os.path.join(test_dir, header)
cpp_path = os.path.join(test_dir, cpp)

main_path = os.path.join(test_dir, 'main.cpp')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write("""#include <QTest>
#include "{}"
QTEST_MAIN({})
""".format(header, class_name))

guard = class_name.upper() + '_H'

with open(header_path, 'w', encoding='utf-8') as f:
    f.write("""#ifndef {}
#define {}
#include <QObject>
class {} : public QObject
{{
    Q_OBJECT
private slots:
}};
#endif // {}
""".format(guard, guard, class_name, guard))

with open(cpp_path, 'w', encoding='utf-8') as f:
    f.write("""#include "{}"
#include <QTest>
""".format(header))

tests_dir = os.path.join(base, 'tests')

dirs = [n for n in os.listdir(tests_dir) if os.path.isdir(os.path.join(tests_dir, n))]

pro_path = os.path.join(tests_dir, 'tests.pro')

with open(pro_path, 'w', encoding='utf-8') as f:
    f.write("""TEMPLATE = subdirs
SUBDIRS += {}
""".format(" ".join(dirs)))