"""
.. module: bless.config.bless_config
    :copyright: (c) 2016 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
"""
import configparser

from bless.config.bless_config import BLESS_OPTIONS_SECTION

CERTIFICATE_VALIDITY_WINDOW_SEC_OPTION = 'certificate_validity_seconds'
CERTIFICATE_VALIDITY_SEC_DEFAULT = 60 * 2

ENTROPY_MINIMUM_BITS_OPTION = 'entropy_minimum_bits'
ENTROPY_MINIMUM_BITS_DEFAULT = 2048

RANDOM_SEED_BYTES_OPTION = 'random_seed_bytes'
RANDOM_SEED_BYTES_DEFAULT = 256

CROSS_ACCOUNT_ROLE_ARN_OPTION = 'cross_account_role_arn'
CROSS_ACCOUNT_ROLE_ARN_DEFAULT = None

LOGGING_LEVEL_OPTION = 'logging_level'
LOGGING_LEVEL_DEFAULT = 'INFO'

CERTIFICATE_TYPE_OPTION = 'certificate_type'
CERTIFICATE_TYPE_DEFAULT = 'user'

BLESS_CA_SECTION = 'Bless CA'
CA_PRIVATE_KEY_FILE_OPTION = 'ca_private_key_file'
KMS_KEY_ID_OPTION = 'kms_key_id'

KMSAUTH_KEY_ID_OPTION = 'kmsauth_key_id'
KMSAUTH_KEY_ID_DEFAULT = None

KMSAUTH_CONTEXT_OPTION = 'kmsauth_context'
KMSAUTH_CONTEXT_DEFAULT = None

REGION_PASSWORD_OPTION_SUFFIX = '_password'


class BlessLyftConfig(configparser.RawConfigParser, object):
    def __init__(self, aws_region, config_file):
        """
        Parses the BLESS config file, and provides some reasonable default values if they are
        absent from the config file.
        The [Bless Options] section is entirely optional, and has defaults.
        The [Bless CA] section is required.
        :param aws_region: The AWS Region BLESS is deployed to.
        :param config_file: Path to the connfig file.
        """
        self.aws_region = aws_region
        defaults = {CERTIFICATE_VALIDITY_WINDOW_SEC_OPTION: CERTIFICATE_VALIDITY_SEC_DEFAULT,
                    ENTROPY_MINIMUM_BITS_OPTION: ENTROPY_MINIMUM_BITS_DEFAULT,
                    RANDOM_SEED_BYTES_OPTION: RANDOM_SEED_BYTES_DEFAULT,
                    CROSS_ACCOUNT_ROLE_ARN_OPTION: CROSS_ACCOUNT_ROLE_ARN_DEFAULT,
                    LOGGING_LEVEL_OPTION: LOGGING_LEVEL_DEFAULT,
                    CERTIFICATE_TYPE_OPTION: CERTIFICATE_TYPE_DEFAULT,
                    KMSAUTH_KEY_ID_OPTION: KMSAUTH_KEY_ID_DEFAULT,
                    KMSAUTH_CONTEXT_OPTION: KMSAUTH_CONTEXT_DEFAULT}
        configparser.RawConfigParser.__init__(self, defaults=defaults)
        self.read(config_file)

        if not self.has_section(BLESS_OPTIONS_SECTION):
            self.add_section(BLESS_OPTIONS_SECTION)

        if not self.has_section(BLESS_CA_SECTION):
            raise ValueError("Can't read config file at: " + config_file)

        if not self.has_option(BLESS_CA_SECTION, self.aws_region + REGION_PASSWORD_OPTION_SUFFIX):
            raise ValueError("No Region Specific Password Provided.")

    def getpassword(self):
        """
        Returns the correct encrypted password based off of the aws_region.
        :return: A Base64 encoded KMS CiphertextBlob.
        """
        return self.get(BLESS_CA_SECTION, self.aws_region + REGION_PASSWORD_OPTION_SUFFIX)