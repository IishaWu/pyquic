from hamcrest import assert_that, is_

from quic.packet import Parser


def describe_parser():
    def describe_parse_public_header():
        def it_advances_data_offset_to_point_to_byte_after_public_header():
            data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08Q025\x12...'
            parser = Parser(data)

            parser.parse_public_header()

            assert_that(parser.data_offset, is_(14))

        def it_extracts_public_flags():
            data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08......'
            parser = Parser(data)

            header = parser.parse_public_header()

            assert_that(header.public_flags, is_(0x08))

        def it_extracts_connection_id():
            data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08......'
            parser = Parser(data)

            header = parser.parse_public_header()

            assert_that(header.connection_id, is_(b'\x01\x02\x03\x04\x05\x06\x07\x08'))

        def it_extracts_protocol_version():
            data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08Q025...'
            parser = Parser(data)

            header = parser.parse_public_header()

            assert_that(header.protocol_version, is_(b'Q025'))

        def describe_when_packet_number_is_1_byte_long():
            def it_extracts_this_one_byte_as_packet_number():
                data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08Q025\x12...'
                parser = Parser(data)

                header = parser.parse_public_header()

                assert_that(header.packet_number, is_(0x12))

        def describe_when_packet_number_is_more_than_1_byte_long():
            def it_extracts_those_bytes_in_little_endian_order():
                data = b'\x18\x01\x02\x03\x04\x05\x06\x07\x08Q025\x34\x12...'
                parser = Parser(data)

                header = parser.parse_public_header()

                assert_that(header.packet_number, is_(0x1234))

    def describe_parse_packet_hash():
        def describe_when_public_header_is_parsed():
            data = b'\x08\x01\x02\x03\x04\x05\x06\x07\x08Q025' \
                b'\x01\x12\x11\x10\x09\x08\x07\x06\x05\x04\x03\x02\x01....'
            parser = Parser(data)
            parser.parse_public_header()

            def it_extracts_12_byte_hash_in_little_endian_encoding():
                packet_hash = parser.parse_packet_hash()

                assert_that(packet_hash, is_(0x010203040506070809101112))

            def it_sets_packet_hash_location():
                parser.parse_packet_hash()

                assert_that(parser.packet_hash_offset, is_(14))
