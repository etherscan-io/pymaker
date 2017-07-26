#!/usr/bin/env python3
#
# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

import pkg_resources
from web3 import Web3, EthereumTesterProvider, TestRPCProvider

from api import Address, Wad
from api.approval import directly
from api.feed import DSValue
from api.sai import Tub
from api.token import DSToken


class ExpTestSaiBite():
    def deploy(self, contract_name, args=None):
        contract_factory = self.web3.eth.contract(abi=json.loads(pkg_resources.resource_string('api.feed', f'abi/{contract_name}.abi')),
                                     bytecode=pkg_resources.resource_string('api.feed', f'abi/{contract_name}.bin'))
        tx_hash = contract_factory.deploy(args=args)
        receipt = self.web3.eth.getTransactionReceipt(tx_hash)
        return receipt['contractAddress']

    def run(self):
        self.web3 = Web3(EthereumTesterProvider())
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        our_account = Address(self.web3.eth.defaultAccount)

        sai = self.deploy('DSToken', ['SAI'])
        sin = self.deploy('DSToken', ['SIN'])
        gem = self.deploy('DSToken', ['ETH'])
        pip = self.deploy('DSValue')
        skr = self.deploy('DSToken', ['SKR'])

        pot = self.deploy('DSVault')
        pit = self.deploy('DSVault')
        tip = self.deploy('Tip')

        dad = self.deploy('DSGuard')
        mom = self.deploy('DSRoles')

        jug = self.deploy('SaiJug', [sai, sin])
        jar = self.deploy('SaiJar', [skr, gem, pip])

        tub = self.deploy('Tub', [jar, jug, pot, pit, tip])
        tap = self.deploy('Tap', [tub, pit])
        top = self.deploy('Top', [tub, tap])

        gem_token = DSToken(web3=self.web3, address=Address(gem))
        print(gem_token.balance_of(our_account))
        gem_token.mint(Wad.from_number(10))
        print(gem_token.balance_of(our_account))

        self.tub = Tub(web3=self.web3, address_tub=Address(tub), address_tap=Address(tap), address_top=Address(top))



        # run test
        self.tub.approve(directly())
        self.tub.join(Wad.from_number(5))


        # pip_contract = DSValue(web3=self.web3, address=Address(pip))
        # print(pip_contract.has_value())
        # pip_contract.poke_with_int(12345)
        # print(pip_contract.has_value())
        # print(pip_contract.read_as_int())




# seth send $SAI_MOM "setRootUser(address,bool)" $ETH_FROM true && seth send $SAI_MOM "setAuthority(address)" $SAI_MOM
#
# export SETH_ASYNC=yes
#
# seth send $SAI_TIP "warp(uint64)" 0
#
# seth send $SAI_TIP "setAuthority(address)" $SAI_MOM
# seth send $SAI_TUB "setAuthority(address)" $SAI_MOM
# seth send $SAI_TAP "setAuthority(address)" $SAI_MOM
# seth send $SAI_TOP "setAuthority(address)" $SAI_MOM
# seth send $SAI_JAR "setAuthority(address)" $SAI_MOM
#
# seth send $SAI_POT "setAuthority(address)" $SAI_DAD
# seth send $SAI_PIT "setAuthority(address)" $SAI_DAD
# seth send $SAI_JUG "setAuthority(address)" $SAI_DAD
#
# seth send $SAI_SAI "setAuthority(address)" $SAI_DAD
# seth send $SAI_SIN "setAuthority(address)" $SAI_DAD
# seth send $SAI_SKR "setAuthority(address)" $SAI_DAD
#
# seth send $SAI_MOM "setUserRole(address,uint8,bool)" $SAI_TUB 255 true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 255 $SAI_JAR $(seth calldata 'join(address,uint128)') true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 255 $SAI_JAR $(seth calldata 'exit(address,uint128)') true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 255 $SAI_JAR $(seth calldata 'push(address,address,uint128)') true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 255 $SAI_JAR $(seth calldata 'pull(address,address,uint128)') true
#
# seth send $SAI_MOM "setUserRole(address,uint8,bool)" $SAI_TOP 254 true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 254 $SAI_JAR $(seth calldata 'push(address,address,uint128)') true
# seth send $SAI_MOM "setRoleCapability(uint8,address,bytes4,bool)" 254 $SAI_TUB $(seth calldata 'cage(uint128)') true
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TUB $SAI_JUG $(seth --to-bytes32 $(seth calldata 'lend(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TUB $SAI_JUG $(seth --to-bytes32 $(seth calldata 'mend(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TUB $SAI_POT $(seth --to-bytes32 $(seth calldata 'push(address,address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TUB $SAI_POT $(seth --to-bytes32 $(seth calldata 'pull(address,address,uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TAP $SAI_JUG $(seth --to-bytes32 $(seth calldata 'heal(address)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TAP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'mint(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TAP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'burn(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TAP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'push(address,address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TAP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'pull(address,address,uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TOP $SAI_JUG $(seth --to-bytes32 $(seth calldata 'heal(address)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TOP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'burn(address)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TOP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'push(address,address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_TOP $SAI_PIT $(seth --to-bytes32 $(seth calldata 'pull(address,address,uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_JAR $SAI_SKR $(seth --to-bytes32 $(seth calldata 'mint(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_JAR $SAI_SKR $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_JUG $SAI_POT $(seth --to-bytes32 $(seth calldata 'mint(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_JUG $SAI_POT $(seth --to-bytes32 $(seth calldata 'burn(address,uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_JUG $SAI_PIT $(seth --to-bytes32 $(seth calldata 'burn(address,uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_POT $SAI_SAI $(seth --to-bytes32 $(seth calldata 'mint(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_POT $SAI_SAI $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_POT $SAI_SIN $(seth --to-bytes32 $(seth calldata 'mint(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_POT $SAI_SIN $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))
#
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_PIT $SAI_SAI $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_PIT $SAI_SIN $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_PIT $SAI_SKR $(seth --to-bytes32 $(seth calldata 'mint(uint128)'))
# seth send $SAI_DAD "permit(address,address,bytes32)" $SAI_PIT $SAI_SKR $(seth --to-bytes32 $(seth calldata 'burn(uint128)'))



        # self.web3
        # print(self.web3.personal.listAccounts)
        # print(self.web3.eth.defaultAccount)


ExpTestSaiBite().run()