import os
import traceback

from click.testing import CliRunner

import config.main as config
import show.main as show
from utilities_common.db import Db

class TestPortChannel(object):
    @classmethod
    def setup_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "1"
        print("SETUP")

    def test_add_portchannel_member_with_invalid_name(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # add a portchannel member with invalid portchannel name
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["add"], ["PortChan005", "Ethernet1"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: PortChan005 is invalid!, name should have prefix 'PortChannel' and suffix '<0-9999>'" in result.output

    def test_delete_portchannel_member_with_invalid_name(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # delete a portchannel member with invalid portchannel name
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["del"], ["PortChan005", "Ethernet1"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: PortChan005 is invalid!, name should have prefix 'PortChannel' and suffix '<0-9999>'" in result.output

    def test_add_non_existing_portchannel_member(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # add a portchannel member with portchannel is not yet created
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["add"], ["PortChannel0005", "Ethernet1"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: PortChannel0005 is not present." in result.output

    def test_delete_non_existing_portchannel_member(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # delete a portchannel member with portchannel is not yet created
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["del"], ["PortChannel0005", "Ethernet1"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: PortChannel0005 is not present." in result.output

    def test_add_portchannel_member_which_has_ipaddress(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # add a portchannel member with port which has ip-address
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["add"], ["PortChannel1001", "Ethernet1"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: Ethernet1 has ip address 14.14.0.1/24 configured" in result.output

    def test_add_portchannel_member_which_is_member_of_vlan(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # add a portchannel member with port which is member of Vlan
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["add"], ["PortChannel1001", "Ethernet24"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: Ethernet24 Interface configured as VLAN_MEMBER under vlan : Vlan2000" in result.output

    def test_add_portchannel_member_which_is_member_of_another_po(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # add a portchannel member with port which is member of another PO
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["add"], ["PortChannel1001", "Ethernet116"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: Ethernet116 Interface is already member of PortChannel0002 " in result.output

    def test_delete_portchannel_member_which_is_member_of_another_po(self):
        runner = CliRunner()
        db = Db()
        obj = {'db':db.cfgdb}

        # delete a portchannel member with port which is member of another PO
        result = runner.invoke(config.config.commands["portchannel"].commands["member"].commands["del"], ["PortChannel1001", "Ethernet116"], obj=obj)
        print(result.exit_code)
        print(result.output)
        assert result.exit_code != 0
        assert "Error: Ethernet116 is not a member of portchannel PortChannel1001" in result.output

    @classmethod
    def teardown_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "0"
        print("TEARDOWN")
