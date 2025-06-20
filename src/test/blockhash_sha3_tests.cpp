#include <boost/test/unit_test.hpp>
#include <test/util/setup_common.h>
#include <primitives/block.h>
#include <uint256.h>

BOOST_FIXTURE_TEST_SUITE(blockhash_sha3_tests, BasicTestingSetup)

BOOST_AUTO_TEST_CASE(default_header_hash)
{
    CBlockHeader header;
    const uint256 expected{"c449874bf12798a85265e027fdae6d670e65a2e74cdd625718a00d52dae3813f"};
    BOOST_CHECK_EQUAL(header.GetHash(), expected);
}

BOOST_AUTO_TEST_SUITE_END()
