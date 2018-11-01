# cedula.py - functions for handling Dominican Republic national identifier
# coding: utf-8
#
# Copyright (C) 2015-2018 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""Cedula (Dominican Republic national identification number).

A cedula is is an 11-digit number issues by the Dominican Republic government
to citizens or residents for identification purposes.

>>> validate('00113918205')
'00113918205'
>>> validate('00113918204')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('0011391820A')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('22400022111')
'224-0002211-1'
"""

from stdnum import luhn
from stdnum.do import rnc
from stdnum.exceptions import *
from stdnum.util import clean


# list of Cedulas that do not match the checksum but are nonetheless valid
whitelist = set('''
00000021249 00000031417 00000035692 00000045342 00000058035 00000065377
00000078587 00000111941 00000126295 00000129963 00000140874 00000144491
00000155482 00000195576 00000236621 00000292212 00000302347 00000404655
00000547495 00000564933 00000669773 00000719400 00001965804 00004110056
00006747587 00010130085 00010628559 00077584000 00100000169 00100012146
00100013114 00100016495 00100053841 00100061611 00100061945 00100074627
00100083860 00100101767 00100126468 00100145737 00100165504 00100169706
00100172940 00100174666 00100181057 00100228718 00100231017 00100238382
00100239662 00100255349 00100288143 00100288929 00100322649 00100336027
00100350928 00100378440 00100384268 00100384523 00100415853 00100430989
00100523399 00100524531 00100530588 00100531007 00100587320 00100590683
00100593378 00100622461 00100664086 00100709215 00100728113 00100729795
00100756082 00100759932 00101118022 00101166065 00101234090 00101527366
00101541404 00101621981 00101659661 00101684656 00101686299 00101821735
00101961125 00102025201 00102398239 00102577448 00102630192 00103266558
00103436936 00103443802 00103754365 00103766231 00103822440 00103983004
00104486903 00104532086 00104662561 00104727362 00104785104 00104862525
00104966313 00105263314 00105328185 00105512386 00105530894 00105606543
00105832408 00106190966 00106284933 00106418989 00106442522 00106479922
00106916538 00107045499 00107075090 00107184305 00107445493 00107602067
00107665688 00107687383 00107691942 00108113363 00108132448 00108184024
00108264871 00108286792 00108384121 00108413431 00108497822 00108784684
00108796883 00108940225 00109183462 00109229090 00109402756 00109785951
00109987435 00110047715 00110071113 00110111536 00110490843 00110578459
00110646203 00111014782 00111150559 00113453700 00114272360 00114532330
00114532355 00114687216 00115039795 00115343847 00116256005 00116448241
00116508511 00117582001 00119161853 00121344165 00121581750 00121581800
00129737056 00130610001 00131257003 00133987848 00134588056 00142864013
00143072001 00144435001 00146965001 00147485003 00149657590 00155144906
00160405001 00161884001 00162906003 00163540003 00163549012 00163709018
00166457056 00166533003 00167311001 00170009162 00170115579 00171404771
00174729003 00174940001 00181880003 00184129003 00189213001 00189405093
00190002567 00196714003 00200021994 00200028716 00200040516 00200063601
00200123640 00200291381 00200409772 00200435544 00200969260 00201023001
00202110760 00202744522 00207327056 00208430205 00208832003 00218507031
00222017001 00235482001 00236245013 00241997013 00246160013 00261011013
00270764013 00274652001 00278005023 00289931003 00291431001 00291549003
00297018001 00298109001 00299724003 00300001538 00300011700 00300013835
00300015531 00300017875 00300019575 00300020806 00300025568 00300040413
00300052890 00300169535 00300244009 00300636564 00301200901 00305535206
00345425001 00352861001 00356533003 00362684023 00376023023 00388338093
00400001552 00400001614 00400012957 00400189811 00409169001 00425759001
00435518003 00475916056 00481106001 00481595003 00493593003 00500335596
00516077003 00520207699 00524571001 00539342005 00540077717 00544657001
00561269169 00572030001 00574599001 00599408003 00633126023 00644236001
00648496171 00651322001 00686904003 00701067521 00720758056 00731054054
00741721056 00757398001 00800106971 00848583056 00857630012 0094662667
00971815056 01000005580 01000250733 01000268998 01000728704 01000855890
01038813907 01094560111 01100014261 01100620962 01103552230 01133025660
01154421047 01200004166 01200008613 01200011252 01200014133 01200027863
01200033420 01200038298 01200771767 01300001142 01300005424 01300020331
01400000282 01400074875 01600009531 01600019983 01600026316 01600027894
01650257001 01700052445 01700200811 01800022457 01800058439 01800527104
01810035037 02038569001 02100061022 02300003061 02300023225 02300031758
02300037618 02300047220 02300052220 02300054193 02300062066 02300085158
02400229955 02500045676 02600036132 02600094954 02700029905 02755972001
02800000129 02800021761 02800025877 02800029588 02831146001 03000411295
03100001162 03100018730 03100034839 03100083297 03100109611 03100156525
03100195659 03100231390 03100232921 03100277078 03100304632 03100332296
03100398552 03100442457 03100486248 03100488033 03100620176 03100654224
03100668294 03100673050 03100771674 03100789636 03100831768 03100963776
03100984652 03101014877 03101070888 03101105802 03101162278 03101409196
03101456639 03101477254 03101577963 03101713684 03101977306 03102342076
03102399233 03102678700 03102805428 03102828522 03102936385 03103202719
03103315310 03103317617 03103749672 03104354892 03107049671 03108309308
03111670001 03121982479 03131503831 03170483480 03200023002 03200066940
03300023841 03400058730 03400157849 03401709701 03500037890 03600046116
03600127038 03600180637 03700663589 03800032522 03807240010 03852380001
03900069856 03900192284 04022130495 04200012900 04400002002 04400627868
04600198229 04700004024 04700020933 04700027064 04700061076 04700070460
04700074827 04700211635 04700221469 04700728184 04701174268 04800019561
04800034846 04800046910 04800956889 04801245892 04900009932 04900011690
04900013913 04900014592 04900026260 04900028443 04900448230 04902549001
04941042001 05100085656 05300013029 05300013204 05300123494 05400016031
05400021759 05400022042 05400028496 05400033166 05400034790 05400037495
05400038776 05400040523 05400047674 05400048248 05400049237 05400049834
05400050196 05400050304 05400052300 05400053627 05400054156 05400055485
05400055770 05400057300 05400057684 05400058964 05400059956 05400060743
05400062459 05400065376 05400067703 05400072273 05400076481 05400216948
05400878578 05500003079 05500006796 05500008806 05500012039 05500014375
05500017761 05500021118 05500022399 05500023407 05500024135 05500024190
05500027749 05500028350 05500032681 05500173451 05500303477 05600037761
05600038251 05600038964 05600051191 05600063115 05600166034 05600267737
05600553831 05700004693 05700064077 05700071202 05900072869 05900105969
06100007818 06100009131 06100011935 06100013662 06100016486 06100017058
06337850001 06400007916 06400011981 06400014372 06400069279 06486186001
06500162568 06800008448 06800245196 06843739551 06900069184 07000007872
07100018031 07100063262 0710208838 07400001254 07401860112 07600000691
07700009346 07800000968 07800002361 08000213172 08016809001 08100002398
08400068380 08498619001 08800002823 08800003986 08800005068 08900001310
08900004344 08900004849 08900005064 08952698001 09000117963 09000169133
09010011235 09022066011 09200533048 09300006239 09300035357 09400022178
09421581768 09500001177 09500003211 09500008222 09700003030 09700179110
09900017864 10061805811 10100178199 10201116357 10462157001 10491297001
10621581792 10983439110 11700000658 12019831001 12300074628 21000000000
22321581834 22721581818 40200401324 40200452735 40200639953 40200700675
58005174058 90001200901
'''.split())


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number provided is a valid cedula."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if number in whitelist:
        return number
    if len(number) != 11:
        raise InvalidLength()
    return luhn.validate(number)


def is_valid(number):
    """Check if the number provided is a valid cedula."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join((number[:3], number[3:-1], number[-1]))


def check_dgii(number, timeout=30):  # pragma: no cover
    """Lookup the number using the DGII online web service.

    This uses the validation service run by the the Dirección General de
    Impuestos Internos, the Dominican Republic tax department to lookup
    registration information for the number. The timeout is in seconds.

    Returns a dict with the following structure::

        {
            'cedula': '12345678901',  # The requested number
            'name': 'The registered name',
            'commercial_name': 'An additional commercial name',
            'status': '2',            # 1: inactive, 2: active
            'category': '0',          # always 0?
            'payment_regime': '2',    # 1: N/D, 2: NORMAL, 3: PST
        }

    Will return None if the number is invalid or unknown."""
    # this function isn't automatically tested because it would require
    # network access for the tests and unnecessarily load the online service
    # we use the RNC implementation and change the rnc result to cedula
    result = rnc.check_dgii(number)
    if result and 'rnc' in result:
        result['cedula'] = result.pop('rnc')
    return result
