// SPDX-License-Identifier: BSD-2-Clause-Views
/*
 * Copyright (c) 2020-2023 The Regents of the University of California
 */

#include "fpga_id.h"

struct fpga_id {
    int id;
    int mask;
    char part[16];
};

const struct fpga_id fpga_id_list[] = 
{
    // Xilinx
    // Spartan 7
    {FPGA_ID_XC7S6,       FPGA_ID_MASK_NOVER, "XC7S6"},
    {FPGA_ID_XC7S15,      FPGA_ID_MASK_NOVER, "XC7S15"},
    {FPGA_ID_XC7S25,      FPGA_ID_MASK_NOVER, "XC7S25"},
    {FPGA_ID_XC7S50,      FPGA_ID_MASK_NOVER, "XC7S50"},
    {FPGA_ID_XC7S75,      FPGA_ID_MASK_NOVER, "XC7S75"},
    {FPGA_ID_XC7S100,     FPGA_ID_MASK_NOVER, "XC7S100"},
    // Artix 7
    {FPGA_ID_XC7A15T,     FPGA_ID_MASK_NOVER, "XC7A15T"},
    {FPGA_ID_XC7A35T,     FPGA_ID_MASK_NOVER, "XC7A35T"},
    {FPGA_ID_XC7A50T,     FPGA_ID_MASK_NOVER, "XC7A50T"},
    {FPGA_ID_XC7A75T,     FPGA_ID_MASK_NOVER, "XC7A75T"},
    {FPGA_ID_XC7A100T,    FPGA_ID_MASK_NOVER, "XC7A100T"},
    {FPGA_ID_XC7A200T,    FPGA_ID_MASK_NOVER, "XC7A200T"},
    // Kintex 7
    {FPGA_ID_XC7K70T,     FPGA_ID_MASK_NOVER, "XC7K70T"},
    {FPGA_ID_XC7K160T,    FPGA_ID_MASK_NOVER, "XC7K160T"},
    {FPGA_ID_XC7K325T,    FPGA_ID_MASK_NOVER, "XC7K325T"},
    {FPGA_ID_XC7K355T,    FPGA_ID_MASK_NOVER, "XC7K355T"},
    {FPGA_ID_XC7K410T,    FPGA_ID_MASK_NOVER, "XC7K410T"},
    {FPGA_ID_XC7K420T,    FPGA_ID_MASK_NOVER, "XC7K420T"},
    {FPGA_ID_XC7K480T,    FPGA_ID_MASK_NOVER, "XC7K480T"},
    // Virtex 7
    {FPGA_ID_XC7V585T,    FPGA_ID_MASK_NOVER, "XC7V585T"},
    {FPGA_ID_XC7V2000T,   FPGA_ID_MASK_NOVER, "XC7V2000T"},
    {FPGA_ID_XC7VX330T,   FPGA_ID_MASK_NOVER, "XC7VX330T"},
    {FPGA_ID_XC7VX415T,   FPGA_ID_MASK_NOVER, "XC7VX415T"},
    {FPGA_ID_XC7VX485T,   FPGA_ID_MASK_NOVER, "XC7VX485T"},
    {FPGA_ID_XC7VX550T,   FPGA_ID_MASK_NOVER, "XC7VX550T"},
    {FPGA_ID_XC7VX690T,   FPGA_ID_MASK_NOVER, "XC7VX690T"},
    {FPGA_ID_XC7VX980T,   FPGA_ID_MASK_NOVER, "XC7VX980T"},
    {FPGA_ID_XC7VX1140T,  FPGA_ID_MASK_NOVER, "XC7VX1140T"},
    {FPGA_ID_XC7VH580T,   FPGA_ID_MASK_NOVER, "XC7VH580T"},
    {FPGA_ID_XC7VH870T,   FPGA_ID_MASK_NOVER, "XC7VH870T"},
    // Zynq 7000
    {FPGA_ID_XC7Z007,     FPGA_ID_MASK_NOVER, "XC7Z007"},
    {FPGA_ID_XC7Z010,     FPGA_ID_MASK_NOVER, "XC7Z010"},
    {FPGA_ID_XC7Z012,     FPGA_ID_MASK_NOVER, "XC7Z012"},
    {FPGA_ID_XC7Z014,     FPGA_ID_MASK_NOVER, "XC7Z014"},
    {FPGA_ID_XC7Z015,     FPGA_ID_MASK_NOVER, "XC7Z015"},
    {FPGA_ID_XC7Z020,     FPGA_ID_MASK_NOVER, "XC7Z020"},
    {FPGA_ID_XC7Z030,     FPGA_ID_MASK_NOVER, "XC7Z030"},
    {FPGA_ID_XC7Z035,     FPGA_ID_MASK_NOVER, "XC7Z035"},
    {FPGA_ID_XC7Z045,     FPGA_ID_MASK_NOVER, "XC7Z045"},
    {FPGA_ID_XC7Z100,     FPGA_ID_MASK_NOVER, "XC7Z100"},
    // Kintex UltraScale
    {FPGA_ID_XCKU025,     FPGA_ID_MASK_NOVER, "XCKU025"},
    {FPGA_ID_XCKU035,     FPGA_ID_MASK_NOVER, "XCKU035"},
    {FPGA_ID_XCKU040,     FPGA_ID_MASK_NOVER, "XCKU040"},
    {FPGA_ID_XCKU060,     FPGA_ID_MASK_NOVER, "XCKU060"},
    {FPGA_ID_XCKU085,     FPGA_ID_MASK_NOVER, "XCKU085"},
    {FPGA_ID_XCKU095,     FPGA_ID_MASK_NOVER, "XCKU095"},
    {FPGA_ID_XCKU115,     FPGA_ID_MASK_NOVER, "XCKU115"},
    // Virtex UltraScale
    {FPGA_ID_XCVU065,     FPGA_ID_MASK_NOVER, "XCVU065"},
    {FPGA_ID_XCVU080,     FPGA_ID_MASK_NOVER, "XCVU080"},
    {FPGA_ID_XCVU095,     FPGA_ID_MASK_NOVER, "XCVU095"},
    {FPGA_ID_XCVU125,     FPGA_ID_MASK_NOVER, "XCVU125"},
    {FPGA_ID_XCVU160,     FPGA_ID_MASK_NOVER, "XCVU160"},
    {FPGA_ID_XCVU190,     FPGA_ID_MASK_NOVER, "XCVU190"},
    {FPGA_ID_XCVU440,     FPGA_ID_MASK_NOVER, "XCVU440"},
    // Artix UltraScale+
    {FPGA_ID_XCAU10P,     FPGA_ID_MASK_NOVER, "XCAU10P"},
    {FPGA_ID_XCAU15P,     FPGA_ID_MASK_NOVER, "XCAU15P"},
    {FPGA_ID_XCAU20P,     FPGA_ID_MASK_NOVER, "XCAU20P"},
    {FPGA_ID_XCAU25P,     FPGA_ID_MASK_NOVER, "XCAU25P"},
    // Kintex UltraScale+
    {FPGA_ID_XCKU3P,      FPGA_ID_MASK_NOVER, "XCKU3P"},
    {FPGA_ID_XCKU5P,      FPGA_ID_MASK_NOVER, "XCKU5P"},
    {FPGA_ID_XCKU9P,      FPGA_ID_MASK_NOVER, "XCKU9P"},
    {FPGA_ID_XCKU11P,     FPGA_ID_MASK_NOVER, "XCKU11P"},
    {FPGA_ID_XCKU13P,     FPGA_ID_MASK_NOVER, "XCKU13P"},
    {FPGA_ID_XCKU15P,     FPGA_ID_MASK_NOVER, "XCKU15P"},
    // Virtex UltraScale+
    {FPGA_ID_XCVU3P,      FPGA_ID_MASK_NOVER, "XCVU3P"},
    {FPGA_ID_XCVU5P,      FPGA_ID_MASK_NOVER, "XCVU5P"},
    {FPGA_ID_XCVU7P,      FPGA_ID_MASK_NOVER, "XCVU7P"},
    {FPGA_ID_XCVU9P,      FPGA_ID_MASK_NOVER, "XCVU9P"},
    {FPGA_ID_XCVU11P,     FPGA_ID_MASK_NOVER, "XCVU11P"},
    {FPGA_ID_XCVU13P,     FPGA_ID_MASK_NOVER, "XCVU13P"},
    {FPGA_ID_XCVU19P,     FPGA_ID_MASK_NOVER, "XCVU19P"},
    {FPGA_ID_XCVU23P,     FPGA_ID_MASK_NOVER, "XCVU23P"},
    {FPGA_ID_XCVU27P,     FPGA_ID_MASK_NOVER, "XCVU27P"},
    {FPGA_ID_XCVU29P,     FPGA_ID_MASK_NOVER, "XCVU29P"},
    {FPGA_ID_XCVU31P,     FPGA_ID_MASK_NOVER, "XCVU31P"},
    {FPGA_ID_XCVU33P,     FPGA_ID_MASK_NOVER, "XCVU33P"},
    {FPGA_ID_XCVU35P,     FPGA_ID_MASK_NOVER, "XCVU35P"},
    {FPGA_ID_XCVU37P,     FPGA_ID_MASK_NOVER, "XCVU37P"},
    {FPGA_ID_XCVU45P,     FPGA_ID_MASK_NOVER, "XCVU45P"},
    {FPGA_ID_XCVU47P,     FPGA_ID_MASK_NOVER, "XCVU47P"},
    {FPGA_ID_XCVU57P,     FPGA_ID_MASK_NOVER, "XCVU57P"},
    // Zynq UltraScale+
    {FPGA_ID_XCZU1,       FPGA_ID_MASK_NOVER, "XCZU1"},
    {FPGA_ID_XCZU2,       FPGA_ID_MASK_NOVER, "XCZU2"},
    {FPGA_ID_XCZU3,       FPGA_ID_MASK_NOVER, "XCZU3"},
    {FPGA_ID_XCZU4,       FPGA_ID_MASK_NOVER, "XCZU4"},
    {FPGA_ID_XCZU5,       FPGA_ID_MASK_NOVER, "XCZU5"},
    {FPGA_ID_XCZU6,       FPGA_ID_MASK_NOVER, "XCZU6"},
    {FPGA_ID_XCZU7,       FPGA_ID_MASK_NOVER, "XCZU7"},
    {FPGA_ID_XCZU9,       FPGA_ID_MASK_NOVER, "XCZU9"},
    {FPGA_ID_XCZU11,      FPGA_ID_MASK_NOVER, "XCZU11"},
    {FPGA_ID_XCZU15,      FPGA_ID_MASK_NOVER, "XCZU15"},
    {FPGA_ID_XCZU17,      FPGA_ID_MASK_NOVER, "XCZU17"},
    {FPGA_ID_XCZU19,      FPGA_ID_MASK_NOVER, "XCZU19"},
    {FPGA_ID_XCZU21,      FPGA_ID_MASK_NOVER, "XCZU21"},
    {FPGA_ID_XCZU25,      FPGA_ID_MASK_NOVER, "XCZU25"},
    {FPGA_ID_XCZU27,      FPGA_ID_MASK_NOVER, "XCZU27"},
    {FPGA_ID_XCZU28,      FPGA_ID_MASK_NOVER, "XCZU28"},
    {FPGA_ID_XCZU29,      FPGA_ID_MASK_NOVER, "XCZU29"},
    {FPGA_ID_XCZU39,      FPGA_ID_MASK_NOVER, "XCZU39"},
    {FPGA_ID_XCZU43,      FPGA_ID_MASK_NOVER, "XCZU43"},
    {FPGA_ID_XCZU46,      FPGA_ID_MASK_NOVER, "XCZU46"},
    {FPGA_ID_XCZU47,      FPGA_ID_MASK_NOVER, "XCZU47"},
    {FPGA_ID_XCZU48,      FPGA_ID_MASK_NOVER, "XCZU48"},
    {FPGA_ID_XCZU49,      FPGA_ID_MASK_NOVER, "XCZU49"},
    {FPGA_ID_XCZU65,      FPGA_ID_MASK_NOVER, "XCZU65"},
    {FPGA_ID_XCZU67,      FPGA_ID_MASK_NOVER, "XCZU67"},
    // Kria SoM (Zynq UltraScale+)
    {FPGA_ID_XCK26,       FPGA_ID_MASK_NOVER, "XCK26"},
    // Alveo (Virtex UltraScale+)
    {FPGA_ID_XCU50,       FPGA_ID_MASK_NOVER, "XCU50"},
    {FPGA_ID_XCU200,      FPGA_ID_MASK_NOVER, "XCU200"},
    {FPGA_ID_XCU250,      FPGA_ID_MASK_NOVER, "XCU250"},
    {FPGA_ID_XCU280,      FPGA_ID_MASK_NOVER, "XCU280"},
    // Versal AI Edge
    {FPGA_ID_XCVE1752,    FPGA_ID_MASK_NOVER, "XCVE1752"},
    {FPGA_ID_XCVE2002,    FPGA_ID_MASK_NOVER, "XCVE2002"},
    {FPGA_ID_XCVE2102,    FPGA_ID_MASK_NOVER, "XCVE2102"},
    {FPGA_ID_XCVE2202,    FPGA_ID_MASK_NOVER, "XCVE2202"},
    {FPGA_ID_XCVE2302,    FPGA_ID_MASK_NOVER, "XCVE2302"},
    {FPGA_ID_XCVE2602,    FPGA_ID_MASK_NOVER, "XCVE2602"},
    {FPGA_ID_XCVE2802,    FPGA_ID_MASK_NOVER, "XCVE2802"},
    // Versal AI Core
    {FPGA_ID_XCVC1352,    FPGA_ID_MASK_NOVER, "XCVC1352"},
    {FPGA_ID_XCVC1502,    FPGA_ID_MASK_NOVER, "XCVC1502"},
    {FPGA_ID_XCVC1702,    FPGA_ID_MASK_NOVER, "XCVC1702"},
    {FPGA_ID_XCVC1802,    FPGA_ID_MASK_NOVER, "XCVC1802"},
    {FPGA_ID_XCVC1902,    FPGA_ID_MASK_NOVER, "XCVC1902"},
    {FPGA_ID_XCVC2602,    FPGA_ID_MASK_NOVER, "XCVC2602"},
    {FPGA_ID_XCVC2802,    FPGA_ID_MASK_NOVER, "XCVC2802"},
    // Versal Prime
    {FPGA_ID_XCVM1102,    FPGA_ID_MASK_NOVER, "XCVM1102"},
    {FPGA_ID_XCVM1302,    FPGA_ID_MASK_NOVER, "XCVM1302"},
    {FPGA_ID_XCVM1402,    FPGA_ID_MASK_NOVER, "XCVM1402"},
    {FPGA_ID_XCVM1502,    FPGA_ID_MASK_NOVER, "XCVM1502"},
    {FPGA_ID_XCVM1802,    FPGA_ID_MASK_NOVER, "XCVM1802"},
    {FPGA_ID_XCVM2202,    FPGA_ID_MASK_NOVER, "XCVM2202"},
    {FPGA_ID_XCVM2302,    FPGA_ID_MASK_NOVER, "XCVM2302"},
    {FPGA_ID_XCVM2502,    FPGA_ID_MASK_NOVER, "XCVM2502"},
    {FPGA_ID_XCVM2902,    FPGA_ID_MASK_NOVER, "XCVM2902"},
    // Versal Premium
    {FPGA_ID_XCVP1002,    FPGA_ID_MASK_NOVER, "XCVP1002"},
    {FPGA_ID_XCVP1052,    FPGA_ID_MASK_NOVER, "XCVP1052"},
    {FPGA_ID_XCVP1102,    FPGA_ID_MASK_NOVER, "XCVP1102"},
    {FPGA_ID_XCVP1202,    FPGA_ID_MASK_NOVER, "XCVP1202"},
    {FPGA_ID_XCVP1402,    FPGA_ID_MASK_NOVER, "XCVP1402"},
    {FPGA_ID_XCVP1502,    FPGA_ID_MASK_NOVER, "XCVP1502"},
    {FPGA_ID_XCVP1552,    FPGA_ID_MASK_NOVER, "XCVP1552"},
    {FPGA_ID_XCVP1702,    FPGA_ID_MASK_NOVER, "XCVP1702"},
    {FPGA_ID_XCVP1802,    FPGA_ID_MASK_NOVER, "XCVP1802"},
    {FPGA_ID_XCVP2502,    FPGA_ID_MASK_NOVER, "XCVP2502"},
    {FPGA_ID_XCVP2802,    FPGA_ID_MASK_NOVER, "XCVP2802"},

    // Intel
    // Stratix 10
    {FPGA_ID_1SG10MH_U1,  FPGA_ID_MASK_FULL,  "1SG10MH_U1"},
    {FPGA_ID_1SG10MH_U2,  FPGA_ID_MASK_FULL,  "1SG10MH_U2"},
    {FPGA_ID_1SG040H,     FPGA_ID_MASK_FULL,  "1SG040H"},
    {FPGA_ID_1SG040H_NL,  FPGA_ID_MASK_FULL,  "1SG040H(NL)"},
    {FPGA_ID_1SG065H,     FPGA_ID_MASK_FULL,  "1SG065H"},
    {FPGA_ID_1SG065H_NL,  FPGA_ID_MASK_FULL,  "1SG065H(NL)"},
    {FPGA_ID_1SG085H,     FPGA_ID_MASK_FULL,  "1SG085H"},
    {FPGA_ID_1SG110H,     FPGA_ID_MASK_FULL,  "1SG110H"},
    {FPGA_ID_1SG110H_NL,  FPGA_ID_MASK_FULL,  "1SG110H(NL)"},
    {FPGA_ID_1SG165H,     FPGA_ID_MASK_FULL,  "1SG165H"},
    {FPGA_ID_1SG166H,     FPGA_ID_MASK_FULL,  "1SG166H"},
    {FPGA_ID_1SG166H_NL,  FPGA_ID_MASK_FULL,  "1SG166H(NL)"},
    {FPGA_ID_1SG210H,     FPGA_ID_MASK_FULL,  "1SG210H"},
    {FPGA_ID_1SG210H_ES1, FPGA_ID_MASK_FULL,  "1SG210H(ES1)"},
    {FPGA_ID_1SG211H,     FPGA_ID_MASK_FULL,  "1SG211H"},
    {FPGA_ID_1SG250L,     FPGA_ID_MASK_FULL,  "1SG250L"},
    {FPGA_ID_1SG250H,     FPGA_ID_MASK_FULL,  "1SG250H"},
    {FPGA_ID_1SG280L,     FPGA_ID_MASK_FULL,  "1SG280L"},
    {FPGA_ID_1SG280L_NL,  FPGA_ID_MASK_FULL,  "1SG280L(NL)"},
    {FPGA_ID_1SG280L_ES1, FPGA_ID_MASK_FULL,  "1SG280L(ES1)"},
    {FPGA_ID_1SG280L_ES2, FPGA_ID_MASK_FULL,  "1SG280L(ES2)"},
    {FPGA_ID_1SG280L_ES3, FPGA_ID_MASK_FULL,  "1SG280L(ES3)"},
    {FPGA_ID_1SG280H,     FPGA_ID_MASK_FULL,  "1SG280H"},
    {FPGA_ID_1SG280H_NL,  FPGA_ID_MASK_FULL,  "1SG280H(NL)"},
    {FPGA_ID_1SG280H_ES1, FPGA_ID_MASK_FULL,  "1SG280H(ES1)"},
    {FPGA_ID_1SG280H_ES2, FPGA_ID_MASK_FULL,  "1SG280H(ES2)"},
    {FPGA_ID_1SG280H_ES3, FPGA_ID_MASK_FULL,  "1SG280H(ES3)"},
    {FPGA_ID_1SX040H,     FPGA_ID_MASK_FULL,  "1SX040H"},
    {FPGA_ID_1SX065H,     FPGA_ID_MASK_FULL,  "1SX065H"},
    {FPGA_ID_1SX085H,     FPGA_ID_MASK_FULL,  "1SX085H"},
    {FPGA_ID_1SX110H,     FPGA_ID_MASK_FULL,  "1SX110H"},
    {FPGA_ID_1SX165H,     FPGA_ID_MASK_FULL,  "1SX165H"},
    {FPGA_ID_1SX210H,     FPGA_ID_MASK_FULL,  "1SX210H"},
    {FPGA_ID_1SX250L,     FPGA_ID_MASK_FULL,  "1SX250L"},
    {FPGA_ID_1SX250H,     FPGA_ID_MASK_FULL,  "1SX250H"},
    {FPGA_ID_1SX280L,     FPGA_ID_MASK_FULL,  "1SX280L"},
    {FPGA_ID_1SX280L_ES1, FPGA_ID_MASK_FULL,  "1SX280L(ES1)"},
    {FPGA_ID_1SX280L_ES2, FPGA_ID_MASK_FULL,  "1SX280L(ES2)"},
    {FPGA_ID_1SX280H,     FPGA_ID_MASK_FULL,  "1SX280H"},
    {FPGA_ID_1SX280H_ES1, FPGA_ID_MASK_FULL,  "1SX280H(ES1)"},
    {FPGA_ID_1SX280H_ES2, FPGA_ID_MASK_FULL,  "1SX280H(ES2)"},
    {FPGA_ID_1ST040E,     FPGA_ID_MASK_FULL,  "1ST040E"},
    {FPGA_ID_1ST040E_NL,  FPGA_ID_MASK_FULL,  "1ST040E(NL)"},
    {FPGA_ID_1ST085E,     FPGA_ID_MASK_FULL,  "1ST085E"},
    {FPGA_ID_1ST110E,     FPGA_ID_MASK_FULL,  "1ST110E"},
    {FPGA_ID_1ST110E_NL,  FPGA_ID_MASK_FULL,  "1ST110E(NL)"},
    {FPGA_ID_1ST165E,     FPGA_ID_MASK_FULL,  "1ST165E"},
    {FPGA_ID_1ST210E,     FPGA_ID_MASK_FULL,  "1ST210E"},
    {FPGA_ID_1ST210E_ES1, FPGA_ID_MASK_FULL,  "1ST210E(ES1)"},
    {FPGA_ID_1ST250E,     FPGA_ID_MASK_FULL,  "1ST250E"},
    {FPGA_ID_1ST280E,     FPGA_ID_MASK_FULL,  "1ST280E"},
    {FPGA_ID_1ST280E_ES1, FPGA_ID_MASK_FULL,  "1ST280E(ES1)"},
    {FPGA_ID_1SM16BE,     FPGA_ID_MASK_FULL,  "1SM16BE"},
    {FPGA_ID_1SM16BE_ES1, FPGA_ID_MASK_FULL,  "1SM16BE(ES1)"},
    {FPGA_ID_1SM16BH,     FPGA_ID_MASK_FULL,  "1SM16BH"},
    {FPGA_ID_1SM16BH_ES1, FPGA_ID_MASK_FULL,  "1SM16BH(ES1)"},
    {FPGA_ID_1SM16CH,     FPGA_ID_MASK_FULL,  "1SM16CH"},
    {FPGA_ID_1SM16CH_ES1, FPGA_ID_MASK_FULL,  "1SM16CH(ES1)"},
    {FPGA_ID_1SM21BE,     FPGA_ID_MASK_FULL,  "1SM21BE"},
    {FPGA_ID_1SM21BE_ES1, FPGA_ID_MASK_FULL,  "1SM21BE(ES1)"},
    {FPGA_ID_1SM21BH,     FPGA_ID_MASK_FULL,  "1SM21BH"},
    {FPGA_ID_1SM21BH_ES1, FPGA_ID_MASK_FULL,  "1SM21BH(ES1)"},
    {FPGA_ID_1SM21CH,     FPGA_ID_MASK_FULL,  "1SM21CH"},
    {FPGA_ID_1SM21CH_ES1, FPGA_ID_MASK_FULL,  "1SM21CH(ES1)"},
    {FPGA_ID_1SD110P,     FPGA_ID_MASK_FULL,  "1SD110P"},
    {FPGA_ID_1SD110P_NL,  FPGA_ID_MASK_FULL,  "1SD110P(NL)"},
    {FPGA_ID_1SD21BP,     FPGA_ID_MASK_FULL,  "1SD21BP"},
    {FPGA_ID_1SD280P,     FPGA_ID_MASK_FULL,  "1SD280P"},
    // Agilex
    {FPGA_ID_AGFA006R16A,    FPGA_ID_MASK_FULL,  "AGFA006R16A"},
    {FPGA_ID_AGFA008R16A,    FPGA_ID_MASK_FULL,  "AGFA008R16A"},
    {FPGA_ID_AGFA012R24A,    FPGA_ID_MASK_FULL,  "AGFA012R24A"},
    {FPGA_ID_AGFA012R24B,    FPGA_ID_MASK_FULL,  "AGFA012R24B"},
    {FPGA_ID_AGFA014R24AR0,  FPGA_ID_MASK_FULL,  "AGFA014R24AR0"},
    {FPGA_ID_AGFA014R24A,    FPGA_ID_MASK_FULL,  "AGFA014R24A"},
    {FPGA_ID_AGFA014R24B,    FPGA_ID_MASK_FULL,  "AGFA014R24B"},
    {FPGA_ID_AGFA019R25A,    FPGA_ID_MASK_FULL,  "AGFA019R25A"},
    {FPGA_ID_AGFA022R24C,    FPGA_ID_MASK_FULL,  "AGFA022R24C"},
    {FPGA_ID_AGFA022R25A,    FPGA_ID_MASK_FULL,  "AGFA022R25A"},
    {FPGA_ID_AGFA022R31C,    FPGA_ID_MASK_FULL,  "AGFA022R31C"},
    {FPGA_ID_AGFA023R25AR0,  FPGA_ID_MASK_FULL,  "AGFA023R25AR0"},
    {FPGA_ID_AGFA023R25A,    FPGA_ID_MASK_FULL,  "AGFA023R25A"},
    {FPGA_ID_AGFA027R24CR0,  FPGA_ID_MASK_FULL,  "AGFA027R24CR0"},
    {FPGA_ID_AGFA027R24CR2,  FPGA_ID_MASK_FULL,  "AGFA027R24CR2"},
    {FPGA_ID_AGFA027R24C,    FPGA_ID_MASK_FULL,  "AGFA027R24C"},
    {FPGA_ID_AGFA027R25AR0,  FPGA_ID_MASK_FULL,  "AGFA027R25AR0"},
    {FPGA_ID_AGFA027R25A,    FPGA_ID_MASK_FULL,  "AGFA027R25A"},
    {FPGA_ID_AGFA027R31C,    FPGA_ID_MASK_FULL,  "AGFA027R31C"},
    {FPGA_ID_AGFB006R16A,    FPGA_ID_MASK_FULL,  "AGFB006R16A"},
    {FPGA_ID_AGFB008R16A,    FPGA_ID_MASK_FULL,  "AGFB008R16A"},
    {FPGA_ID_AGFB012R24A,    FPGA_ID_MASK_FULL,  "AGFB012R24A"},
    {FPGA_ID_AGFB012R24B,    FPGA_ID_MASK_FULL,  "AGFB012R24B"},
    {FPGA_ID_AGFB014R24AR0,  FPGA_ID_MASK_FULL,  "AGFB014R24AR0"},
    {FPGA_ID_AGFB014R24A,    FPGA_ID_MASK_FULL,  "AGFB014R24A"},
    {FPGA_ID_AGFB014R24B,    FPGA_ID_MASK_FULL,  "AGFB014R24B"},
    {FPGA_ID_AGFB019R25A,    FPGA_ID_MASK_FULL,  "AGFB019R25A"},
    {FPGA_ID_AGFB022R24C,    FPGA_ID_MASK_FULL,  "AGFB022R24C"},
    {FPGA_ID_AGFB022R25A,    FPGA_ID_MASK_FULL,  "AGFB022R25A"},
    {FPGA_ID_AGFB022R31C,    FPGA_ID_MASK_FULL,  "AGFB022R31C"},
    {FPGA_ID_AGFB023R25AR0,  FPGA_ID_MASK_FULL,  "AGFB023R25AR0"},
    {FPGA_ID_AGFB023R25A,    FPGA_ID_MASK_FULL,  "AGFB023R25A"},
    {FPGA_ID_AGFB027R24CR0,  FPGA_ID_MASK_FULL,  "AGFB027R24CR0"},
    {FPGA_ID_AGFB027R24CR2,  FPGA_ID_MASK_FULL,  "AGFB027R24CR2"},
    {FPGA_ID_AGFB027R24C,    FPGA_ID_MASK_FULL,  "AGFB027R24C"},
    {FPGA_ID_AGFB027R25AR0,  FPGA_ID_MASK_FULL,  "AGFB027R25AR0"},
    {FPGA_ID_AGFB027R25A,    FPGA_ID_MASK_FULL,  "AGFB027R25A"},
    {FPGA_ID_AGFB027R31C,    FPGA_ID_MASK_FULL,  "AGFB027R31C"},
    {FPGA_ID_AGFC019R25A,    FPGA_ID_MASK_FULL,  "AGFC019R25A"},
    {FPGA_ID_AGFC023R25AR0,  FPGA_ID_MASK_FULL,  "AGFC023R25AR0"},
    {FPGA_ID_AGFC023R25A,    FPGA_ID_MASK_FULL,  "AGFC023R25A"},
    {FPGA_ID_AGFD019R25A,    FPGA_ID_MASK_FULL,  "AGFD019R25A"},
    {FPGA_ID_AGFD023R25AR0,  FPGA_ID_MASK_FULL,  "AGFD023R25AR0"},
    {FPGA_ID_AGFD023R25A,    FPGA_ID_MASK_FULL,  "AGFD023R25A"},
    {FPGA_ID_AGIB022R29A,    FPGA_ID_MASK_FULL,  "AGIB022R29A"},
    {FPGA_ID_AGIB022R31B,    FPGA_ID_MASK_FULL,  "AGIB022R31B"},
    {FPGA_ID_AGIB027R29AR0,  FPGA_ID_MASK_FULL,  "AGIB027R29AR0"},
    {FPGA_ID_AGIB027R29AR1,  FPGA_ID_MASK_FULL,  "AGIB027R29AR1"},
    {FPGA_ID_AGIB027R29AR3,  FPGA_ID_MASK_FULL,  "AGIB027R29AR3"},
    {FPGA_ID_AGIB027R29A,    FPGA_ID_MASK_FULL,  "AGIB027R29A"},
    {FPGA_ID_AGIB027R31BR0,  FPGA_ID_MASK_FULL,  "AGIB027R31BR0"},
    {FPGA_ID_AGIB027R31B,    FPGA_ID_MASK_FULL,  "AGIB027R31B"},

    // end of list
    {0, 0, ""}
};

const char *get_fpga_part(int id)
{
    const struct fpga_id *ptr = fpga_id_list;

    while (ptr->id && ((ptr->id ^ id) & ptr->mask) != 0)
    {
        ptr++;
    }

    return ptr->part;
}

