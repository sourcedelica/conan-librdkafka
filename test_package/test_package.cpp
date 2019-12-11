#include <iostream>
#include "librdkafka/rdkafkacpp.h"

int main()
{
    RdKafka::Conf *conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);
    return 0;
}
