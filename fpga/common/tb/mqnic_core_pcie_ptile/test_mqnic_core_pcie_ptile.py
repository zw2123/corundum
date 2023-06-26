# SPDX-License-Identifier: BSD-2-Clause-Views
# Copyright (c) 2022-2023 The Regents of the University of California

import logging
import os
import sys

import scapy.utils
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP

import cocotb_test.simulator
import pytest

import cocotb
from cocotb.log import SimLog
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

from cocotbext.axi import AxiStreamBus
from cocotbext.axi import AxiSlave, AxiBus, SparseMemoryRegion
from cocotbext.eth import EthMac
from cocotbext.pcie.core import RootComplex
from cocotbext.pcie.intel.ptile import PTilePcieDevice, PTileRxBus, PTileTxBus

try:
    import mqnic
except ImportError:
    # attempt import from current directory
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    try:
        import mqnic
    finally:
        del sys.path[0]


class TB(object):
    def __init__(self, dut, msix_count=32):
        self.dut = dut

        self.log = SimLog("cocotb.tb")
        self.log.setLevel(logging.DEBUG)

        # PCIe
        self.rc = RootComplex()

        self.rc.max_payload_size = 0x1  # 256 bytes
        self.rc.max_read_request_size = 0x2  # 512 bytes

        self.dev = PTilePcieDevice(
            # configuration options
            pcie_generation=3,
            # pcie_link_width=2,
            # pld_clk_frequency=250e6,
            pf_count=1,
            max_payload_size=512,
            enable_extended_tag=True,

            pf0_msi_enable=False,
            pf0_msi_count=1,
            pf1_msi_enable=False,
            pf1_msi_count=1,
            pf2_msi_enable=False,
            pf2_msi_count=1,
            pf3_msi_enable=False,
            pf3_msi_count=1,
            pf0_msix_enable=True,
            pf0_msix_table_size=msix_count-1,
            pf0_msix_table_bir=0,
            pf0_msix_table_offset=0x00010000,
            pf0_msix_pba_bir=0,
            pf0_msix_pba_offset=0x00018000,
            pf1_msix_enable=False,
            pf1_msix_table_size=0,
            pf1_msix_table_bir=0,
            pf1_msix_table_offset=0x00000000,
            pf1_msix_pba_bir=0,
            pf1_msix_pba_offset=0x00000000,
            pf2_msix_enable=False,
            pf2_msix_table_size=0,
            pf2_msix_table_bir=0,
            pf2_msix_table_offset=0x00000000,
            pf2_msix_pba_bir=0,
            pf2_msix_pba_offset=0x00000000,
            pf3_msix_enable=False,
            pf3_msix_table_size=0,
            pf3_msix_table_bir=0,
            pf3_msix_table_offset=0x00000000,
            pf3_msix_pba_bir=0,
            pf3_msix_pba_offset=0x00000000,

            # signals
            # Clock and reset
            reset_status=dut.rst,
            # reset_status_n=dut.reset_status_n,
            coreclkout_hip=dut.clk,
            # refclk0=dut.refclk0,
            # refclk1=dut.refclk1,
            # pin_perst_n=dut.pin_perst_n,

            # RX interface
            rx_bus=PTileRxBus.from_prefix(dut, "rx_st"),
            # rx_par_err=dut.rx_par_err,

            # TX interface
            tx_bus=PTileTxBus.from_prefix(dut, "tx_st"),
            # tx_par_err=dut.tx_par_err,

            # RX flow control
            rx_buffer_limit=dut.rx_buffer_limit,
            rx_buffer_limit_tdm_idx=dut.rx_buffer_limit_tdm_idx,

            # TX flow control
            tx_cdts_limit=dut.tx_cdts_limit,
            tx_cdts_limit_tdm_idx=dut.tx_cdts_limit_tdm_idx,

            # Power management and hard IP status interface
            # link_up=dut.link_up,
            # dl_up=dut.dl_up,
            # surprise_down_err=dut.surprise_down_err,
            # ltssm_state=dut.ltssm_state,
            # pm_state=dut.pm_state,
            # pm_dstate=dut.pm_dstate,
            # apps_pm_xmt_pme=dut.apps_pm_xmt_pme,
            # app_req_retry_en=dut.app_req_retry_en,

            # Interrupt interface
            # app_int=dut.app_int,
            # msi_pnd_func=dut.msi_pnd_func,
            # msi_pnd_byte=dut.msi_pnd_byte,
            # msi_pnd_addr=dut.msi_pnd_addr,

            # Error interface
            # serr_out=dut.serr_out,
            # hip_enter_err_mode=dut.hip_enter_err_mode,
            # app_err_valid=dut.app_err_valid,
            # app_err_hdr=dut.app_err_hdr,
            # app_err_info=dut.app_err_info,
            # app_err_func_num=dut.app_err_func_num,

            # Completion timeout interface
            # cpl_timeout=dut.cpl_timeout,
            # cpl_timeout_avmm_clk=dut.cpl_timeout_avmm_clk,
            # cpl_timeout_avmm_address=dut.cpl_timeout_avmm_address,
            # cpl_timeout_avmm_read=dut.cpl_timeout_avmm_read,
            # cpl_timeout_avmm_readdata=dut.cpl_timeout_avmm_readdata,
            # cpl_timeout_avmm_readdatavalid=dut.cpl_timeout_avmm_readdatavalid,
            # cpl_timeout_avmm_write=dut.cpl_timeout_avmm_write,
            # cpl_timeout_avmm_writedata=dut.cpl_timeout_avmm_writedata,
            # cpl_timeout_avmm_waitrequest=dut.cpl_timeout_avmm_waitrequest,

            # Configuration output
            tl_cfg_func=dut.tl_cfg_func,
            tl_cfg_add=dut.tl_cfg_add,
            tl_cfg_ctl=dut.tl_cfg_ctl,
            # dl_timer_update=dut.dl_timer_update,

            # Configuration intercept interface
            # cii_req=dut.cii_req,
            # cii_hdr_poisoned=dut.cii_hdr_poisoned,
            # cii_hdr_first_be=dut.cii_hdr_first_be,
            # cii_func_num=dut.cii_func_num,
            # cii_wr_vf_active=dut.cii_wr_vf_active,
            # cii_vf_num=dut.cii_vf_num,
            # cii_wr=dut.cii_wr,
            # cii_addr=dut.cii_addr,
            # cii_dout=dut.cii_dout,
            # cii_override_en=dut.cii_override_en,
            # cii_override_din=dut.cii_override_din,
            # cii_halt=dut.cii_halt,

            # Hard IP reconfiguration interface
            # hip_reconfig_clk=dut.hip_reconfig_clk,
            # hip_reconfig_address=dut.hip_reconfig_address,
            # hip_reconfig_read=dut.hip_reconfig_read,
            # hip_reconfig_readdata=dut.hip_reconfig_readdata,
            # hip_reconfig_readdatavalid=dut.hip_reconfig_readdatavalid,
            # hip_reconfig_write=dut.hip_reconfig_write,
            # hip_reconfig_writedata=dut.hip_reconfig_writedata,
            # hip_reconfig_waitrequest=dut.hip_reconfig_waitrequest,

            # Page request service
            # prs_event_valid=dut.prs_event_valid,
            # prs_event_func=dut.prs_event_func,
            # prs_event=dut.prs_event,

            # SR-IOV (VF error)
            # vf_err_ur_posted_s0=dut.vf_err_ur_posted_s0,
            # vf_err_ur_posted_s1=dut.vf_err_ur_posted_s1,
            # vf_err_ur_posted_s2=dut.vf_err_ur_posted_s2,
            # vf_err_ur_posted_s3=dut.vf_err_ur_posted_s3,
            # vf_err_func_num_s0=dut.vf_err_func_num_s0,
            # vf_err_func_num_s1=dut.vf_err_func_num_s1,
            # vf_err_func_num_s2=dut.vf_err_func_num_s2,
            # vf_err_func_num_s3=dut.vf_err_func_num_s3,
            # vf_err_ca_postedreq_s0=dut.vf_err_ca_postedreq_s0,
            # vf_err_ca_postedreq_s1=dut.vf_err_ca_postedreq_s1,
            # vf_err_ca_postedreq_s2=dut.vf_err_ca_postedreq_s2,
            # vf_err_ca_postedreq_s3=dut.vf_err_ca_postedreq_s3,
            # vf_err_vf_num_s0=dut.vf_err_vf_num_s0,
            # vf_err_vf_num_s1=dut.vf_err_vf_num_s1,
            # vf_err_vf_num_s2=dut.vf_err_vf_num_s2,
            # vf_err_vf_num_s3=dut.vf_err_vf_num_s3,
            # vf_err_poisonedwrreq_s0=dut.vf_err_poisonedwrreq_s0,
            # vf_err_poisonedwrreq_s1=dut.vf_err_poisonedwrreq_s1,
            # vf_err_poisonedwrreq_s2=dut.vf_err_poisonedwrreq_s2,
            # vf_err_poisonedwrreq_s3=dut.vf_err_poisonedwrreq_s3,
            # vf_err_poisonedcompl_s0=dut.vf_err_poisonedcompl_s0,
            # vf_err_poisonedcompl_s1=dut.vf_err_poisonedcompl_s1,
            # vf_err_poisonedcompl_s2=dut.vf_err_poisonedcompl_s2,
            # vf_err_poisonedcompl_s3=dut.vf_err_poisonedcompl_s3,
            # user_vfnonfatalmsg_func_num=dut.user_vfnonfatalmsg_func_num,
            # user_vfnonfatalmsg_vfnum=dut.user_vfnonfatalmsg_vfnum,
            # user_sent_vfnonfatalmsg=dut.user_sent_vfnonfatalmsg,
            # vf_err_overflow=dut.vf_err_overflow,

            # FLR
            # flr_rcvd_pf=dut.flr_rcvd_pf,
            # flr_rcvd_vf=dut.flr_rcvd_vf,
            # flr_rcvd_pf_num=dut.flr_rcvd_pf_num,
            # flr_rcvd_vf_num=dut.flr_rcvd_vf_num,
            # flr_completed_pf=dut.flr_completed_pf,
            # flr_completed_vf=dut.flr_completed_vf,
            # flr_completed_pf_num=dut.flr_completed_pf_num,
            # flr_completed_vf_num=dut.flr_completed_vf_num,

            # VirtIO
            # virtio_pcicfg_vfaccess=dut.virtio_pcicfg_vfaccess,
            # virtio_pcicfg_vfnum=dut.virtio_pcicfg_vfnum,
            # virtio_pcicfg_pfnum=dut.virtio_pcicfg_pfnum,
            # virtio_pcicfg_bar=dut.virtio_pcicfg_bar,
            # virtio_pcicfg_length=dut.virtio_pcicfg_length,
            # virtio_pcicfg_baroffset=dut.virtio_pcicfg_baroffset,
            # virtio_pcicfg_cfgdata=dut.virtio_pcicfg_cfgdata,
            # virtio_pcicfg_cfgwr=dut.virtio_pcicfg_cfgwr,
            # virtio_pcicfg_cfgrd=dut.virtio_pcicfg_cfgrd,
            # virtio_pcicfg_appvfnum=dut.virtio_pcicfg_appvfnum,
            # virtio_pcicfg_apppfnum=dut.virtio_pcicfg_apppfnum,
            # virtio_pcicfg_rdack=dut.virtio_pcicfg_rdack,
            # virtio_pcicfg_rdbe=dut.virtio_pcicfg_rdbe,
            # virtio_pcicfg_data=dut.virtio_pcicfg_data,
        )

        # self.dev.log.setLevel(logging.DEBUG)

        self.rc.make_port().connect(self.dev)

        self.driver = mqnic.Driver()

        self.dev.functions[0].configure_bar(0, 2**len(dut.core_pcie_inst.axil_ctrl_araddr), ext=True, prefetch=True)
        if hasattr(dut.core_pcie_inst, 'pcie_app_ctrl'):
            self.dev.functions[0].configure_bar(2, 2**len(dut.core_pcie_inst.axil_app_ctrl_araddr), ext=True, prefetch=True)

        core_inst = dut.core_pcie_inst.core_inst

        # Ethernet
        self.port_mac = []

        eth_int_if_width = len(core_inst.m_axis_tx_tdata) / len(core_inst.m_axis_tx_tvalid)
        eth_clock_period = 6.4
        eth_speed = 10e9

        if eth_int_if_width == 64:
            # 10G
            eth_clock_period = 6.4
            eth_speed = 10e9
        elif eth_int_if_width == 128:
            # 25G
            eth_clock_period = 2.56
            eth_speed = 25e9
        elif eth_int_if_width == 512:
            # 100G
            eth_clock_period = 3.102
            eth_speed = 100e9

        for iface in core_inst.iface:
            for k in range(len(iface.port)):
                cocotb.start_soon(Clock(iface.port[k].port_rx_clk, eth_clock_period, units="ns").start())
                cocotb.start_soon(Clock(iface.port[k].port_tx_clk, eth_clock_period, units="ns").start())

                iface.port[k].port_rx_rst.setimmediatevalue(0)
                iface.port[k].port_tx_rst.setimmediatevalue(0)

                mac = EthMac(
                    tx_clk=iface.port[k].port_tx_clk,
                    tx_rst=iface.port[k].port_tx_rst,
                    tx_bus=AxiStreamBus.from_prefix(iface.interface_inst.port[k].port_inst.port_tx_inst, "m_axis_tx"),
                    tx_ptp_time=iface.port[k].port_tx_ptp_ts_96,
                    tx_ptp_ts=iface.interface_inst.port[k].port_inst.port_tx_inst.s_axis_tx_cpl_ts,
                    tx_ptp_ts_tag=iface.interface_inst.port[k].port_inst.port_tx_inst.s_axis_tx_cpl_tag,
                    tx_ptp_ts_valid=iface.interface_inst.port[k].port_inst.port_tx_inst.s_axis_tx_cpl_valid,
                    rx_clk=iface.port[k].port_rx_clk,
                    rx_rst=iface.port[k].port_rx_rst,
                    rx_bus=AxiStreamBus.from_prefix(iface.interface_inst.port[k].port_inst.port_rx_inst, "s_axis_rx"),
                    rx_ptp_time=iface.port[k].port_rx_ptp_ts_96,
                    ifg=12, speed=eth_speed
                )

                self.port_mac.append(mac)

        dut.eth_tx_status.setimmediatevalue(2**len(core_inst.m_axis_tx_tvalid)-1)
        dut.eth_rx_status.setimmediatevalue(2**len(core_inst.m_axis_tx_tvalid)-1)

        # DDR
        self.ddr_group_size = core_inst.DDR_GROUP_SIZE.value
        self.ddr_ram = []
        self.ddr_axi_if = []
        if hasattr(core_inst, 'ddr'):
            ram = None
            for i, ch in enumerate(core_inst.ddr.dram_if_inst.ch):
                cocotb.start_soon(Clock(ch.ch_clk, 3.332, units="ns").start())
                ch.ch_rst.setimmediatevalue(0)
                ch.ch_status.setimmediatevalue(1)

                if i % self.ddr_group_size == 0:
                    ram = SparseMemoryRegion()
                    self.ddr_ram.append(ram)
                self.ddr_axi_if.append(AxiSlave(AxiBus.from_prefix(ch, "axi_ch"), ch.ch_clk, ch.ch_rst, target=ram))

        # HBM
        self.hbm_group_size = core_inst.HBM_GROUP_SIZE.value
        self.hbm_ram = []
        self.hbm_axi_if = []
        if hasattr(core_inst, 'hbm'):
            ram = None
            for i, ch in enumerate(core_inst.hbm.dram_if_inst.ch):
                cocotb.start_soon(Clock(ch.ch_clk, 2.222, units="ns").start())
                ch.ch_rst.setimmediatevalue(0)
                ch.ch_status.setimmediatevalue(1)

                if i % self.hbm_group_size == 0:
                    ram = SparseMemoryRegion()
                    self.hbm_ram.append(ram)
                self.hbm_axi_if.append(AxiSlave(AxiBus.from_prefix(ch, "axi_ch"), ch.ch_clk, ch.ch_rst, target=ram))

        dut.ctrl_reg_wr_wait.setimmediatevalue(0)
        dut.ctrl_reg_wr_ack.setimmediatevalue(0)
        dut.ctrl_reg_rd_data.setimmediatevalue(0)
        dut.ctrl_reg_rd_wait.setimmediatevalue(0)
        dut.ctrl_reg_rd_ack.setimmediatevalue(0)

        cocotb.start_soon(Clock(dut.ptp_clk, 6.4, units="ns").start())
        dut.ptp_rst.setimmediatevalue(0)
        cocotb.start_soon(Clock(dut.ptp_sample_clk, 8, units="ns").start())

        dut.s_axis_stat_tdata.setimmediatevalue(0)
        dut.s_axis_stat_tid.setimmediatevalue(0)
        dut.s_axis_stat_tvalid.setimmediatevalue(0)

        self.loopback_enable = False
        cocotb.start_soon(self._run_loopback())

    async def init(self):

        for mac in self.port_mac:
            mac.rx.reset.setimmediatevalue(0)
            mac.tx.reset.setimmediatevalue(0)

        self.dut.ptp_rst.setimmediatevalue(0)

        for ram in self.ddr_axi_if + self.ddr_axi_if:
            ram.write_if.reset.setimmediatevalue(0)

        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)

        for mac in self.port_mac:
            mac.rx.reset.setimmediatevalue(1)
            mac.tx.reset.setimmediatevalue(1)

        self.dut.ptp_rst.setimmediatevalue(1)

        for ram in self.ddr_axi_if + self.ddr_axi_if:
            ram.write_if.reset.setimmediatevalue(1)

        await FallingEdge(self.dut.rst)
        await Timer(100, 'ns')

        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)

        for mac in self.port_mac:
            mac.rx.reset.setimmediatevalue(0)
            mac.tx.reset.setimmediatevalue(0)

        self.dut.ptp_rst.setimmediatevalue(0)

        for ram in self.ddr_axi_if + self.ddr_axi_if:
            ram.write_if.reset.setimmediatevalue(0)

        await self.rc.enumerate()

    async def _run_loopback(self):
        while True:
            await RisingEdge(self.dut.clk)

            if self.loopback_enable:
                for mac in self.port_mac:
                    if not mac.tx.empty():
                        await mac.rx.send(await mac.tx.recv())


@cocotb.test()
async def run_test_nic(dut):

    tb = TB(dut, msix_count=2**len(dut.core_pcie_inst.irq_index))

    await tb.init()

    tb.log.info("Init driver")
    await tb.driver.init_pcie_dev(tb.rc.find_device(tb.dev.functions[0].pcie_id))
    for interface in tb.driver.interfaces:
        await interface.open()

    # enable queues
    tb.log.info("Enable queues")
    for interface in tb.driver.interfaces:
        await interface.sched_blocks[0].schedulers[0].rb.write_dword(mqnic.MQNIC_RB_SCHED_RR_REG_CTRL, 0x00000001)
        for k in range(len(interface.txq)):
            await interface.sched_blocks[0].schedulers[0].hw_regs.write_dword(4*k, 0x00000003)

    # wait for all writes to complete
    await tb.driver.hw_regs.read_dword(0)
    tb.log.info("Init complete")

    tb.log.info("Send and receive single packet")

    for interface in tb.driver.interfaces:
        data = bytearray([x % 256 for x in range(1024)])

        await interface.start_xmit(data, 0)

        pkt = await tb.port_mac[interface.index*interface.port_count].tx.recv()
        tb.log.info("Packet: %s", pkt)

        await tb.port_mac[interface.index*interface.port_count].rx.send(pkt)

        pkt = await interface.recv()

        tb.log.info("Packet: %s", pkt)
        if interface.if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

    tb.log.info("RX and TX checksum tests")

    payload = bytes([x % 256 for x in range(256)])
    eth = Ether(src='5A:51:52:53:54:55', dst='DA:D1:D2:D3:D4:D5')
    ip = IP(src='192.168.1.100', dst='192.168.1.101')
    udp = UDP(sport=1, dport=2)
    test_pkt = eth / ip / udp / payload

    if tb.driver.interfaces[0].if_feature_tx_csum:
        test_pkt2 = test_pkt.copy()
        test_pkt2[UDP].chksum = scapy.utils.checksum(bytes(test_pkt2[UDP]))

        await tb.driver.interfaces[0].start_xmit(test_pkt2.build(), 0, 34, 6)
    else:
        await tb.driver.interfaces[0].start_xmit(test_pkt.build(), 0)

    pkt = await tb.port_mac[0].tx.recv()
    tb.log.info("Packet: %s", pkt)

    await tb.port_mac[0].rx.send(pkt)

    pkt = await tb.driver.interfaces[0].recv()

    tb.log.info("Packet: %s", pkt)
    if tb.driver.interfaces[0].if_feature_rx_csum:
        assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff
    assert Ether(pkt.data).build() == test_pkt.build()

    tb.log.info("Queue mapping offset test")

    data = bytearray([x % 256 for x in range(1024)])

    tb.loopback_enable = True

    for k in range(4):
        await tb.driver.interfaces[0].set_rx_queue_map_indir_table(0, 0, k)

        await tb.driver.interfaces[0].start_xmit(data, 0)

        pkt = await tb.driver.interfaces[0].recv()

        tb.log.info("Packet: %s", pkt)
        if tb.driver.interfaces[0].if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff
        assert pkt.queue == k

    tb.loopback_enable = False

    await tb.driver.interfaces[0].set_rx_queue_map_indir_table(0, 0, 0)

    if tb.driver.interfaces[0].if_feature_rss:
        tb.log.info("Queue mapping RSS mask test")

        await tb.driver.interfaces[0].set_rx_queue_map_rss_mask(0, 0x00000003)

        for k in range(4):
            await tb.driver.interfaces[0].set_rx_queue_map_indir_table(0, k, k)

        tb.loopback_enable = True

        queues = set()

        for k in range(64):
            payload = bytes([x % 256 for x in range(256)])
            eth = Ether(src='5A:51:52:53:54:55', dst='DA:D1:D2:D3:D4:D5')
            ip = IP(src='192.168.1.100', dst='192.168.1.101')
            udp = UDP(sport=1, dport=k+0)
            test_pkt = eth / ip / udp / payload

            if tb.driver.interfaces[0].if_feature_tx_csum:
                test_pkt2 = test_pkt.copy()
                test_pkt2[UDP].chksum = scapy.utils.checksum(bytes(test_pkt2[UDP]))

                await tb.driver.interfaces[0].start_xmit(test_pkt2.build(), 0, 34, 6)
            else:
                await tb.driver.interfaces[0].start_xmit(test_pkt.build(), 0)

        for k in range(64):
            pkt = await tb.driver.interfaces[0].recv()

            tb.log.info("Packet: %s", pkt)
            if tb.driver.interfaces[0].if_feature_rx_csum:
                assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

            queues.add(pkt.queue)

        assert len(queues) == 4

        tb.loopback_enable = False

        await tb.driver.interfaces[0].set_rx_queue_map_rss_mask(0, 0)

    tb.log.info("Multiple small packets")

    count = 64

    pkts = [bytearray([(x+k) % 256 for x in range(60)]) for k in range(count)]

    tb.loopback_enable = True

    for p in pkts:
        await tb.driver.interfaces[0].start_xmit(p, 0)

    for k in range(count):
        pkt = await tb.driver.interfaces[0].recv()

        tb.log.info("Packet: %s", pkt)
        assert pkt.data == pkts[k]
        if tb.driver.interfaces[0].if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

    tb.loopback_enable = False

    tb.log.info("Multiple TX queues")

    count = 1024

    pkts = [bytearray([(x+k) % 256 for x in range(60)]) for k in range(count)]

    tb.loopback_enable = True

    for k in range(len(pkts)):
        await tb.driver.interfaces[0].start_xmit(pkts[k], k % len(tb.driver.interfaces[0].txq))

    for k in range(count):
        pkt = await tb.driver.interfaces[0].recv()

        tb.log.info("Packet: %s", pkt)
        if tb.driver.interfaces[0].if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

    tb.loopback_enable = False

    tb.log.info("Multiple large packets")

    count = 64

    pkts = [bytearray([(x+k) % 256 for x in range(1514)]) for k in range(count)]

    tb.loopback_enable = True

    for p in pkts:
        await tb.driver.interfaces[0].start_xmit(p, 0)

    for k in range(count):
        pkt = await tb.driver.interfaces[0].recv()

        tb.log.info("Packet: %s", pkt)
        assert pkt.data == pkts[k]
        if tb.driver.interfaces[0].if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

    tb.loopback_enable = False

    tb.log.info("Jumbo frames")

    count = 64

    pkts = [bytearray([(x+k) % 256 for x in range(9014)]) for k in range(count)]

    tb.loopback_enable = True

    for p in pkts:
        await tb.driver.interfaces[0].start_xmit(p, 0)

    for k in range(count):
        pkt = await tb.driver.interfaces[0].recv()

        tb.log.info("Packet: %s", pkt)
        assert pkt.data == pkts[k]
        if tb.driver.interfaces[0].if_feature_rx_csum:
            assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

    tb.loopback_enable = False

    if len(tb.driver.interfaces) > 1:
        tb.log.info("All interfaces")

        count = 64

        pkts = [bytearray([(x+k) % 256 for x in range(1514)]) for k in range(count)]

        tb.loopback_enable = True

        for k, p in enumerate(pkts):
            await tb.driver.interfaces[k % len(tb.driver.interfaces)].start_xmit(p, 0)

        for k in range(count):
            pkt = await tb.driver.interfaces[k % len(tb.driver.interfaces)].recv()

            tb.log.info("Packet: %s", pkt)
            assert pkt.data == pkts[k]
            if tb.driver.interfaces[0].if_feature_rx_csum:
                assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

        tb.loopback_enable = False

    if len(tb.driver.interfaces[0].sched_blocks) > 1:
        tb.log.info("All interface 0 scheduler blocks")

        for block in tb.driver.interfaces[0].sched_blocks:
            await block.schedulers[0].rb.write_dword(mqnic.MQNIC_RB_SCHED_RR_REG_CTRL, 0x00000001)
            await tb.driver.interfaces[0].set_rx_queue_map_indir_table(block.index, 0, block.index)
            for k in range(len(block.interface.txq)):
                if k % len(tb.driver.interfaces[0].sched_blocks) == block.index:
                    await block.schedulers[0].hw_regs.write_dword(4*k, 0x00000003)
                else:
                    await block.schedulers[0].hw_regs.write_dword(4*k, 0x00000000)

        count = 64

        pkts = [bytearray([(x+k) % 256 for x in range(1514)]) for k in range(count)]

        tb.loopback_enable = True

        queues = set()

        for k, p in enumerate(pkts):
            await tb.driver.interfaces[0].start_xmit(p, k % len(tb.driver.interfaces[0].sched_blocks))

        for k in range(count):
            pkt = await tb.driver.interfaces[0].recv()

            tb.log.info("Packet: %s", pkt)
            # assert pkt.data == pkts[k]
            if tb.driver.interfaces[0].if_feature_rx_csum:
                assert pkt.rx_checksum == ~scapy.utils.checksum(bytes(pkt.data[14:])) & 0xffff

            queues.add(pkt.queue)

        assert len(queues) == len(tb.driver.interfaces[0].sched_blocks)

        tb.loopback_enable = False

        for block in tb.driver.interfaces[0].sched_blocks[1:]:
            await block.schedulers[0].rb.write_dword(mqnic.MQNIC_RB_SCHED_RR_REG_CTRL, 0x00000000)
            await tb.driver.interfaces[0].set_rx_queue_map_indir_table(block.index, 0, 0)

    tb.log.info("Read statistics counters")

    await Timer(2000, 'ns')

    lst = []

    for k in range(64):
        lst.append(await tb.driver.hw_regs.read_dword(0x020000+k*8))

    print(lst)

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)


# cocotb-test

tests_dir = os.path.dirname(__file__)
rtl_dir = os.path.abspath(os.path.join(tests_dir, '..', '..', 'rtl'))
lib_dir = os.path.abspath(os.path.join(rtl_dir, '..', 'lib'))
axi_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'axi', 'rtl'))
axis_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'axis', 'rtl'))
eth_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'eth', 'rtl'))
pcie_rtl_dir = os.path.abspath(os.path.join(lib_dir, 'pcie', 'rtl'))


@pytest.mark.parametrize(("if_count", "ports_per_if", "pcie_data_width",
        "axis_eth_data_width", "axis_eth_sync_data_width", "ptp_ts_enable"), [
            (1, 1, 256, 64, 64, 1),
            (1, 1, 256, 64, 64, 0),
            (2, 1, 256, 64, 64, 1),
            (1, 2, 256, 64, 64, 1),
            (1, 1, 256, 64, 128, 1),
            (1, 1, 512, 64, 64, 1),
            (1, 1, 512, 64, 128, 1),
            (1, 1, 512, 512, 512, 1),
        ])
def test_mqnic_core_pcie_ptile(request, if_count, ports_per_if, pcie_data_width,
        axis_eth_data_width, axis_eth_sync_data_width, ptp_ts_enable):
    dut = "mqnic_core_pcie_ptile"
    module = os.path.splitext(os.path.basename(__file__))[0]
    toplevel = dut

    verilog_sources = [
        os.path.join(rtl_dir, f"{dut}.v"),
        os.path.join(rtl_dir, "mqnic_core_pcie.v"),
        os.path.join(rtl_dir, "mqnic_core.v"),
        os.path.join(rtl_dir, "mqnic_dram_if.v"),
        os.path.join(rtl_dir, "mqnic_interface.v"),
        os.path.join(rtl_dir, "mqnic_interface_tx.v"),
        os.path.join(rtl_dir, "mqnic_interface_rx.v"),
        os.path.join(rtl_dir, "mqnic_port.v"),
        os.path.join(rtl_dir, "mqnic_port_tx.v"),
        os.path.join(rtl_dir, "mqnic_port_rx.v"),
        os.path.join(rtl_dir, "mqnic_egress.v"),
        os.path.join(rtl_dir, "mqnic_ingress.v"),
        os.path.join(rtl_dir, "mqnic_l2_egress.v"),
        os.path.join(rtl_dir, "mqnic_l2_ingress.v"),
        os.path.join(rtl_dir, "mqnic_rx_queue_map.v"),
        os.path.join(rtl_dir, "mqnic_ptp.v"),
        os.path.join(rtl_dir, "mqnic_ptp_clock.v"),
        os.path.join(rtl_dir, "mqnic_ptp_perout.v"),
        os.path.join(rtl_dir, "mqnic_rb_clk_info.v"),
        os.path.join(rtl_dir, "cpl_write.v"),
        os.path.join(rtl_dir, "cpl_op_mux.v"),
        os.path.join(rtl_dir, "desc_fetch.v"),
        os.path.join(rtl_dir, "desc_op_mux.v"),
        os.path.join(rtl_dir, "event_mux.v"),
        os.path.join(rtl_dir, "queue_manager.v"),
        os.path.join(rtl_dir, "cpl_queue_manager.v"),
        os.path.join(rtl_dir, "tx_fifo.v"),
        os.path.join(rtl_dir, "rx_fifo.v"),
        os.path.join(rtl_dir, "tx_req_mux.v"),
        os.path.join(rtl_dir, "tx_engine.v"),
        os.path.join(rtl_dir, "rx_engine.v"),
        os.path.join(rtl_dir, "tx_checksum.v"),
        os.path.join(rtl_dir, "rx_hash.v"),
        os.path.join(rtl_dir, "rx_checksum.v"),
        os.path.join(rtl_dir, "stats_counter.v"),
        os.path.join(rtl_dir, "stats_collect.v"),
        os.path.join(rtl_dir, "stats_pcie_if.v"),
        os.path.join(rtl_dir, "stats_pcie_tlp.v"),
        os.path.join(rtl_dir, "stats_dma_if_pcie.v"),
        os.path.join(rtl_dir, "stats_dma_latency.v"),
        os.path.join(rtl_dir, "mqnic_tx_scheduler_block_rr.v"),
        os.path.join(rtl_dir, "tx_scheduler_rr.v"),
        os.path.join(eth_rtl_dir, "ptp_clock.v"),
        os.path.join(eth_rtl_dir, "ptp_clock_cdc.v"),
        os.path.join(eth_rtl_dir, "ptp_perout.v"),
        os.path.join(axi_rtl_dir, "axil_crossbar.v"),
        os.path.join(axi_rtl_dir, "axil_crossbar_addr.v"),
        os.path.join(axi_rtl_dir, "axil_crossbar_rd.v"),
        os.path.join(axi_rtl_dir, "axil_crossbar_wr.v"),
        os.path.join(axi_rtl_dir, "axil_reg_if.v"),
        os.path.join(axi_rtl_dir, "axil_reg_if_rd.v"),
        os.path.join(axi_rtl_dir, "axil_reg_if_wr.v"),
        os.path.join(axi_rtl_dir, "axil_register_rd.v"),
        os.path.join(axi_rtl_dir, "axil_register_wr.v"),
        os.path.join(axi_rtl_dir, "arbiter.v"),
        os.path.join(axi_rtl_dir, "priority_encoder.v"),
        os.path.join(axis_rtl_dir, "axis_adapter.v"),
        os.path.join(axis_rtl_dir, "axis_arb_mux.v"),
        os.path.join(axis_rtl_dir, "axis_async_fifo.v"),
        os.path.join(axis_rtl_dir, "axis_async_fifo_adapter.v"),
        os.path.join(axis_rtl_dir, "axis_demux.v"),
        os.path.join(axis_rtl_dir, "axis_fifo.v"),
        os.path.join(axis_rtl_dir, "axis_fifo_adapter.v"),
        os.path.join(axis_rtl_dir, "axis_pipeline_fifo.v"),
        os.path.join(axis_rtl_dir, "axis_register.v"),
        os.path.join(pcie_rtl_dir, "pcie_axil_master.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_demux.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_demux_bar.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_mux.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fc_count.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fifo.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fifo_raw.v"),
        os.path.join(pcie_rtl_dir, "pcie_tlp_fifo_mux.v"),
        os.path.join(pcie_rtl_dir, "pcie_msix.v"),
        os.path.join(pcie_rtl_dir, "irq_rate_limit.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie_rd.v"),
        os.path.join(pcie_rtl_dir, "dma_if_pcie_wr.v"),
        os.path.join(pcie_rtl_dir, "dma_if_mux.v"),
        os.path.join(pcie_rtl_dir, "dma_if_mux_rd.v"),
        os.path.join(pcie_rtl_dir, "dma_if_mux_wr.v"),
        os.path.join(pcie_rtl_dir, "dma_if_desc_mux.v"),
        os.path.join(pcie_rtl_dir, "dma_ram_demux_rd.v"),
        os.path.join(pcie_rtl_dir, "dma_ram_demux_wr.v"),
        os.path.join(pcie_rtl_dir, "dma_psdpram.v"),
        os.path.join(pcie_rtl_dir, "dma_client_axis_sink.v"),
        os.path.join(pcie_rtl_dir, "dma_client_axis_source.v"),
        os.path.join(pcie_rtl_dir, "pcie_ptile_if.v"),
        os.path.join(pcie_rtl_dir, "pcie_ptile_if_rx.v"),
        os.path.join(pcie_rtl_dir, "pcie_ptile_if_tx.v"),
        os.path.join(pcie_rtl_dir, "pcie_ptile_cfg.v"),
        os.path.join(pcie_rtl_dir, "pcie_ptile_fc_counter.v"),
        os.path.join(pcie_rtl_dir, "pulse_merge.v"),
    ]

    parameters = {}

    # Structural configuration
    parameters['IF_COUNT'] = if_count
    parameters['PORTS_PER_IF'] = ports_per_if
    parameters['SCHED_PER_IF'] = ports_per_if

    # Clock configuration
    parameters['CLK_PERIOD_NS_NUM'] = 4
    parameters['CLK_PERIOD_NS_DENOM'] = 1

    # PTP configuration
    parameters['PTP_CLK_PERIOD_NS_NUM'] = 32
    parameters['PTP_CLK_PERIOD_NS_DENOM'] = 5
    parameters['PTP_CLOCK_PIPELINE'] = 0
    parameters['PTP_CLOCK_CDC_PIPELINE'] = 0
    parameters['PTP_USE_SAMPLE_CLOCK'] = 1
    parameters['PTP_SEPARATE_TX_CLOCK'] = 0
    parameters['PTP_SEPARATE_RX_CLOCK'] = 0
    parameters['PTP_PORT_CDC_PIPELINE'] = 0
    parameters['PTP_PEROUT_ENABLE'] = 0
    parameters['PTP_PEROUT_COUNT'] = 1

    # Queue manager configuration
    parameters['EVENT_QUEUE_OP_TABLE_SIZE'] = 32
    parameters['TX_QUEUE_OP_TABLE_SIZE'] = 32
    parameters['RX_QUEUE_OP_TABLE_SIZE'] = 32
    parameters['TX_CPL_QUEUE_OP_TABLE_SIZE'] = parameters['TX_QUEUE_OP_TABLE_SIZE']
    parameters['RX_CPL_QUEUE_OP_TABLE_SIZE'] = parameters['RX_QUEUE_OP_TABLE_SIZE']
    parameters['EVENT_QUEUE_INDEX_WIDTH'] = 6
    parameters['TX_QUEUE_INDEX_WIDTH'] = 13
    parameters['RX_QUEUE_INDEX_WIDTH'] = 8
    parameters['TX_CPL_QUEUE_INDEX_WIDTH'] = parameters['TX_QUEUE_INDEX_WIDTH']
    parameters['RX_CPL_QUEUE_INDEX_WIDTH'] = parameters['RX_QUEUE_INDEX_WIDTH']
    parameters['EVENT_QUEUE_PIPELINE'] = 3
    parameters['TX_QUEUE_PIPELINE'] = 3 + max(parameters['TX_QUEUE_INDEX_WIDTH']-12, 0)
    parameters['RX_QUEUE_PIPELINE'] = 3 + max(parameters['RX_QUEUE_INDEX_WIDTH']-12, 0)
    parameters['TX_CPL_QUEUE_PIPELINE'] = parameters['TX_QUEUE_PIPELINE']
    parameters['RX_CPL_QUEUE_PIPELINE'] = parameters['RX_QUEUE_PIPELINE']

    # TX and RX engine configuration
    parameters['TX_DESC_TABLE_SIZE'] = 32
    parameters['RX_DESC_TABLE_SIZE'] = 32
    parameters['RX_INDIR_TBL_ADDR_WIDTH'] = min(parameters['RX_QUEUE_INDEX_WIDTH'], 8)

    # Scheduler configuration
    parameters['TX_SCHEDULER_OP_TABLE_SIZE'] = parameters['TX_DESC_TABLE_SIZE']
    parameters['TX_SCHEDULER_PIPELINE'] = parameters['TX_QUEUE_PIPELINE']
    parameters['TDMA_INDEX_WIDTH'] = 6

    # Interface configuration
    parameters['PTP_TS_ENABLE'] = ptp_ts_enable
    parameters['TX_CPL_ENABLE'] = parameters['PTP_TS_ENABLE']
    parameters['TX_CPL_FIFO_DEPTH'] = 32
    parameters['TX_TAG_WIDTH'] = 16
    parameters['TX_CHECKSUM_ENABLE'] = 1
    parameters['RX_HASH_ENABLE'] = 1
    parameters['RX_CHECKSUM_ENABLE'] = 1
    parameters['TX_FIFO_DEPTH'] = 32768
    parameters['RX_FIFO_DEPTH'] = 131072
    parameters['MAX_TX_SIZE'] = 9214
    parameters['MAX_RX_SIZE'] = 9214
    parameters['TX_RAM_SIZE'] = 131072
    parameters['RX_RAM_SIZE'] = 131072

    # RAM configuration
    parameters['DDR_CH'] = 1
    parameters['DDR_ENABLE'] = 0
    parameters['DDR_GROUP_SIZE'] = 1
    parameters['AXI_DDR_DATA_WIDTH'] = 256
    parameters['AXI_DDR_ADDR_WIDTH'] = 32
    parameters['AXI_DDR_ID_WIDTH'] = 8
    parameters['AXI_DDR_MAX_BURST_LEN'] = 256
    parameters['HBM_CH'] = 1
    parameters['HBM_ENABLE'] = 0
    parameters['HBM_GROUP_SIZE'] = parameters['HBM_CH']
    parameters['AXI_HBM_DATA_WIDTH'] = 256
    parameters['AXI_HBM_ADDR_WIDTH'] = 32
    parameters['AXI_HBM_ID_WIDTH'] = 6
    parameters['AXI_HBM_MAX_BURST_LEN'] = 16

    # Application block configuration
    parameters['APP_ID'] = 0x00000000
    parameters['APP_ENABLE'] = 0
    parameters['APP_CTRL_ENABLE'] = 1
    parameters['APP_DMA_ENABLE'] = 1
    parameters['APP_AXIS_DIRECT_ENABLE'] = 1
    parameters['APP_AXIS_SYNC_ENABLE'] = 1
    parameters['APP_AXIS_IF_ENABLE'] = 1
    parameters['APP_STAT_ENABLE'] = 1

    # DMA interface configuration
    parameters['DMA_IMM_ENABLE'] = 0
    parameters['DMA_IMM_WIDTH'] = 32
    parameters['DMA_LEN_WIDTH'] = 16
    parameters['DMA_TAG_WIDTH'] = 16
    parameters['RAM_ADDR_WIDTH'] = (max(parameters['TX_RAM_SIZE'], parameters['RX_RAM_SIZE'])-1).bit_length()
    parameters['RAM_PIPELINE'] = 2

    # PCIe interface configuration
    parameters['SEG_COUNT'] = 2 if pcie_data_width == 512 else 1
    parameters['SEG_DATA_WIDTH'] = pcie_data_width // parameters['SEG_COUNT']
    parameters['SEG_EMPTY_WIDTH'] = ((parameters['SEG_DATA_WIDTH'] // 32) - 1).bit_length()
    parameters['SEG_HDR_WIDTH'] = 128
    parameters['SEG_PRFX_WIDTH'] = 32
    parameters['TX_SEQ_NUM_WIDTH'] = 6
    parameters['TX_SEQ_NUM_ENABLE'] = 1
    parameters['PF_COUNT'] = 1
    parameters['VF_COUNT'] = 0
    parameters['PCIE_TAG_COUNT'] = 256
    parameters['PCIE_DMA_READ_OP_TABLE_SIZE'] = parameters['PCIE_TAG_COUNT']
    parameters['PCIE_DMA_READ_TX_LIMIT'] = 2**parameters['TX_SEQ_NUM_WIDTH']
    parameters['PCIE_DMA_WRITE_OP_TABLE_SIZE'] = 2**parameters['TX_SEQ_NUM_WIDTH']
    parameters['PCIE_DMA_WRITE_TX_LIMIT'] = 2**parameters['TX_SEQ_NUM_WIDTH']

    # Interrupt configuration
    parameters['IRQ_INDEX_WIDTH'] = parameters['EVENT_QUEUE_INDEX_WIDTH']

    # AXI lite interface configuration (control)
    parameters['AXIL_CTRL_DATA_WIDTH'] = 32
    parameters['AXIL_CTRL_ADDR_WIDTH'] = 24
    parameters['AXIL_CSR_PASSTHROUGH_ENABLE'] = 0

    # AXI lite interface configuration (application control)
    parameters['AXIL_APP_CTRL_DATA_WIDTH'] = parameters['AXIL_CTRL_DATA_WIDTH']
    parameters['AXIL_APP_CTRL_ADDR_WIDTH'] = 24

    # Ethernet interface configuration
    parameters['AXIS_ETH_DATA_WIDTH'] = axis_eth_data_width
    parameters['AXIS_ETH_SYNC_DATA_WIDTH'] = axis_eth_sync_data_width
    parameters['AXIS_ETH_RX_USE_READY'] = 0
    parameters['AXIS_ETH_TX_PIPELINE'] = 0
    parameters['AXIS_ETH_TX_FIFO_PIPELINE'] = 2
    parameters['AXIS_ETH_TX_TS_PIPELINE'] = 0
    parameters['AXIS_ETH_RX_PIPELINE'] = 0
    parameters['AXIS_ETH_RX_FIFO_PIPELINE'] = 2

    # Statistics counter subsystem
    parameters['STAT_ENABLE'] = 1
    parameters['STAT_DMA_ENABLE'] = 1
    parameters['STAT_PCIE_ENABLE'] = 1
    parameters['STAT_INC_WIDTH'] = 24
    parameters['STAT_ID_WIDTH'] = 12

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    sim_build = os.path.join(tests_dir, "sim_build",
        request.node.name.replace('[', '-').replace(']', ''))

    cocotb_test.simulator.run(
        python_search=[tests_dir],
        verilog_sources=verilog_sources,
        toplevel=toplevel,
        module=module,
        parameters=parameters,
        sim_build=sim_build,
        extra_env=extra_env,
    )
