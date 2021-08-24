#ifndef TESTFOO_H
#define TESTFOO_H
#include <QObject>
class TestFoo : public QObject
{
    Q_OBJECT
private slots:
    void test();
};
#endif // TESTFOO_H
