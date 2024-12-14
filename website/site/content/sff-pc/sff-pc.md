+++
title = "A guide to SSF PCs"
description = "A guide to SSF PCs"
date = 2024-10-22T00:00:00Z
draft = false

[taxonomies]
tags = ["Features","SSF","Tiny","Thinkcentre"]
[extra]
keywords = "SSF, Tiny, Embed, Embedded, Streamable"
toc = true
series = "Features"
+++

# A guide to SSF PCs

Welcome to the guide to SSF PCs.

## Introduction into SSF PCs

In this section, we will see the different aspects of SSF PCs and his components.

### What is an SSF PC?

An SSF PC is a **Small Form Factor PC**, it usually very compact, power efficient, and can be used for various purposes, they are usually used in schools, offices and homes servers.

### Why should I choose an SSF PC?

There are many reasons to choose an SSF PC:

- **Compact**: SSF PCs are very compact, they can be placed anywhere.
- **Power efficient**: SSF PCs are generally power efficient (like T or U series processors).
- **Cheap**: SSF PCs are usually cheaper than traditional PCs.

### Why shouldn't I choose an SSF PC?

There are some reasons not to choose an SSF PC:

- **Limited upgrade/change options**: SSF PCs have limited upgrade/change options, you can't upgrade/change to newer components.
- **Limited ports**: SSF PCs have limited ports.
- **Limited performance**: SSF PCs have limited performance due to their small size and thermal constraints.
- **Proprietary components**: SSF PCs have proprietary components, you can't replace them with standard components.

### What are some examples of SSF PCs?

Some brands and models of SSF PCs:

- **Lenovo Thinkcentre**: M73 tiny, M710q, M720q, M70q G1, M75q G1, M90q G3 etc.
- **Dell Optiplex**: 3040, 3050, 3060, 3070, 5040, 5050, 5060, 5070 etc.
- **HP EliteDesk**: 800 G1 mini, 800 G2 mini etc.
- **Intel NUC**: NUC6i3SYH, NUC6i5SYH, NUC6i7KYK, NUC7i3BNH, NUC7i5BNH, NUC7i7BNH etc.
- **Zotac ZBOX**: CI660 nano, CI640 nano, CI620 nano, CI540 nano, CI520 nano, CI327 nano etc.
- **Asus VivoMini**: UN65, UN65U, UN65U-M023M, UN65U-M021M, UN65U-M022M, UN65U-M020M etc.

Many other brands and models are available on the market.

I recommend the **Lenovo, Dell, HP**, there are plenty of them on the second-hand market, pretty cheap and generally upgradable (RAM, SSD, CPU, PSU).

### ARM SSP PCs

SSP PCs are often in x86 but for several years now, ARM SSP PCs are more and more popular, they are generally cheaper, more power efficient, but have limited software compatibility (Not x86/PC compatible), upgrade options and performance.

In this guide, we will focus on x86 SSP PCs and Raspberry Pi.

## SSF PCs components

In this section, we will see the components of SSF PCs.

### CPU (Central Processing Unit)

I recommend using socketed CPUs, they are upgradable to more powerfull CPU (with same TDP), you can for example upgrade from **intel celeron G4900T** to **intel i9 9900T** without any issue.

Most SSF PCs have 35W or 65W CPUs, **i really recommend to avoid put a CPU with more than the maximum TDP supported by the SSF PC**, it can cause overheating and damage the motherboard or the PSU.

Nowadays, most software use AVX, AVX2 instructions, you can easily multiply the performance by 2 or 3 times, especially for video encoding/decoding, compression, encryption, etc... Every CPU since **intel Haswell** and **AMD Zen** support AVX2 (except some low-end CPUs like **intel celeron/pentium** and **AMD Athlon**).

| Brand | CPU arch | CPU Gen | Socket | RAM Type | Max RAM | Year | Exemple of SSF PC | Remarks |
|---------|------------|----------|----------|------------|-----------|--------|------------------|---------|
| intel | Merom | Core 2 | LGA775 | DDR2 | 8GB | 2006-2007 | | Huge performance improvement over Netburst |
| intel | Penryn | Core 2 | LGA775 | DDR2 | 8GB | 2007-2008 | | Better power efficiency |
| intel | Nehalem | 1st Gen | LGA1156 | DDR3 | 16GB | 2008-2009 | | SMT, Memory controller on CPU and monolithic quad-core |
| intel | Westmere | 1st Gen | LGA1156 | DDR3 | 16GB | 2010-2011 | | Better power efficiency |
| intel | Sandy Bridge | 2nd Gen | LGA1155 | DDR3 | 32GB | 2011-2012 | M72 tiny | Add AVX support, good iGPU and greatly improve perf |
| intel | Ivy Bridge | 3rd Gen | LGA1155 | DDR3 | 32GB | 2012-2013 | M72 tiny | Better power efficiency |
| intel | Haswell | 4th Gen | LGA1150 | DDR3 | 32GB | 2013-2014 | M73 tiny | Support AVX2 and FMA3, improve perf |
| intel | Broadwell | 5th Gen | LGA1150 | DDR3 | 32GB | 2014-2015 | | Better power efficiency |
| intel | Skylake | 6th Gen | LGA1151 | DDR4 | 64GB | 2015-2016 | M710q | HEVC/VP9 8-bit hardware enc/dec, iGPU vulkan and NVMe support |
| intel | Kaby Lake | 7th Gen | LGA1151 | DDR4 | 64GB | 2016-2017 | M710q | HEVC/VP9 10-bit hardware enc/dec support |
| intel | Coffee Lake | 8-9th Gen | LGA1151 | DDR4 | 64GB | 2017-2019 | M720q | Increase core count and remove hyperthreading on 9th gen CPUs |
| intel | Comet Lake | 10th Gen | LGA1200 | DDR4 | 128GB | 2020-2021 | M70G gen 1 | Re-add hyperthreading on most CPUs |
| intel | Rocket Lake | 11th Gen | LGA1200 | DDR4 | 128GB | 2021-2022 | M70G gen 2 | Add AVX-512 support and better perf |
| intel | Alder Lake | 12th Gen | LGA1700 | DDR5 | 256GB | 2021-2022 | M70G gen 3 | Remove AVX-512, Pcore and ECore, AV1 hardware dec support and improve IPC |
| intel | Raptor Lake | 13-14th Gen | LGA1700 | DDR5 | 256GB | 2022-2023 | M70G gen 4 | |
| intel | Arrow Lake | 15th Gen | LGA1700 | DDR5 | 256GB | 2023-2024 | M70G gen 5 | Remove SMT and greatly improve efficiency |
| AMD | Excavator | 4th Gen | AM4 | DDR4 | 32GB | 2015-2016 | | |
| AMD | Zen | 1st Gen | AM4 | DDR4 | 64GB | 2017-2018 | M715Q | Huge performance improvement and on pair with intel Haswell CPUs |
| AMD | Zen+ | 2nd Gen | AM4 | DDR4 | 64GB | 2018-2019 | | |
| AMD | Zen 2 | 3rd Gen | AM4 | DDR4 | 128GB | 2019-2020 | | On pair with intel Skylake CPUs and fix most of the issues of Zen |
| AMD | Zen 3 | 4th Gen | AM4 | DDR4 | 128GB | 2020-2021 | | Improve IPC and power efficiency |
| AMD | Zen 4 | 5th Gen | AM5 | DDR5 | 256GB | 2021-2022 | | Add AVX-512 support and better IPC |
| AMD | Zen 5 | 6th Gen | AM5 | DDR5 | 256GB | 2022-2023 | | Slightly improve IPC |

I recommend using **Intel Skylake**, **AMD Zen 2**, or newer CPUs, as they offer good performance and support modern features like: NVMe, iGPU vulkan, HEVC/VP9 10-bit hardware enc/dec, AVX2 etc...
However, if you’re on a budget, Haswell remains a good option due the low price of the CPUs, DDR3 RAM and relatively good performance.

### GPU (Graphics Processing Unit)

Most SSF PCs have only integrated GPU, they are generally enough for light GPU tasks and consume very low power, great for home servers or office PCs.

Some SSF PCs can have a dedicated GPU (Like the M720Q/M920Q), they are mostly in low profile and have PCIe x4/x8 lanes, it can be useful for light gaming, Networking etc... Ensure the PSU and motherboard can support it the GPU power consumption.

### RAM (Random Access Memory)

For SSF PCs, you generally have 2 RAM slots, you can use DDR3, DDR4 RAM or DDR5 RAM, the maximum capacity is generally 16GB to 128GB depending on the CPU, i recommend using two same RAM sticks, it help to improve stability and performance (dual channel, double the bandwidth).

You can take highter frequency RAM than the CPU support, the RAM will be downclocked to the CPU supported frequency, juste ensure the RAM generation is supported by the CPU and RAM slots (DDR3, DDR4, DDR5).

### Storage

SSF PCs have 4 storage options (depending on the model):

- **M.2 NVMe SSD**: They are very fast and they are present in most SSF PCs* (since 2015), the optimal choice.
- **M.2 SATA SSD**: Use same connector as NVMe but slower with SATA interface (In thinkcentre M700 for example).
- **2.5" SATA SSD**: They are slower than M.2 SSD but it's a good choice if you can't use M.2 SSD.
- **2.5" SATA HDD**: They are very slow and generally not recommended, but they can be easily replaced by SSD.
- **On board eMMC**: On motherboard memory, **you should avoid it**, it's generally slow, limited and once it's dead, you must replace the motherboard.

I recommend using **M.2 NVMe SSDs**, beware of the size (2242, 2260, 2280), the key (B, M, B+M) and simple or double sided.

### Ports

All SSF PCs have a limited number of ports, you must ensure the SSF PC have enough ports for your needs, some SSF PCs can have extension cards to add more ports (Like the M720Q).

### PSU (Power Supply Unit)

Most SSF PCs have an external power supply, often have a proprietary connector, 65W is anough for 35W CPU, 90W is enough for 65W CPU, 135W for 65W CPU + 45W GPU ect... Just ensure the PSU is anough to support the CPU (and extension card) power consumption.

### Motherboard

Like PSU, most SSF PCs have a proprietary motherboard, sometimes you can replace it with another model of same brand (Like M920Q motherboard in M720Q), most of the time, just keep the same motherboard model.

## Lenovo thinkcentre SSF PCs

In this section, we will see the different models of Lenovo thinkcentre SSF PCs.

| Model | CPU | Chipset | SODIMM RAM | PCIe | Drive | Remarks |
|-------|-----|---------|------------|------|--------|--------|
| M72 tiny | ivy bridge | Intel H61 | 2x 8GB 1600MHz DDR3 | No | 1x 2.5" | |
| M92 tiny | ivy bridge | Intel Q77 | 2x 8GB 1600MHz DDR3 | No | 1x 2.5" | |
| M73 tiny | Haswell | Intel H81 | 2x 8GB 1600MHz DDR3 | No | 1x 2.5" | |
| M83 tiny | Haswell | Intel Q85 | 2x 8GB 1600MHz DDR3 | No | 1x 2.5" | |
| M700q | Skylake | Intel B150 | 2x 32GB 2133MHz DDR4 | No | 1x m.2 **SATA**, 1x 2.5" | |
| M900q | Skylake | Intel Q170 | 2x 32GB 2133MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M710q | Skylake/Kaby Lake | Intel B250 | 2x 32GB 2400MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M910q | Skylake/Kaby Lake | Intel Q270 | 2x 32GB 2400MHz DDR4 | No | 2x m.2, 1x 2.5" | |
| M720q | Coffee Lake | Intel B360 | 2x 32GB 2666MHz DDR4 | PCIe x8 Gen 3 | 1x m.2, 1x 2.5" | |
| M920q| Coffee Lake | Intel Q370 | 2x 32GB 2666MHz DDR4 | PCIe x8 Gen 3 | 1x m.2, 1x 2.5" | |
| M920x | Coffee Lake | Intel Q370 | 2x 32GB 2666MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| P330 | Coffee Lake | Intel Q370 | 2x 32GB 2666MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| M75q | AMD Zen 2 | AMD Pro 500 | 2x 32GB 2933MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M75q Gen 2 | AMD Zen 3 | AMD Pro 500 | 2x 32GB 3200MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M70q | Comet Lake | Intel H470 | 2x 32GB 2933MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M80q | Comet Lake | Intel Q470 | 2x 32GB 2933MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M90q | Comet Lake | Intel Q470 | 2x 32GB 2933MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| P340 | Comet Lake | Intel Q470 | 2x 32GB 2933MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| M70q Gen 2 | Rocket Lake | Intel B560 | 2x 32GB 3200MHz DDR4 | No | 1x m.2, 1x 2.5" | |
| M90q Gen 2 | Rocket Lake | Intel Q570 | 2x 32GB 3200MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| P350 | Rocket Lake | Intel Q570 | 2x 32GB 3200MHz DDR4 | PCIe x8 Gen 3 | 2x m.2, 1x 2.5" | |
| M80q Gen 3 | Alder Lake | Intel Q670 | 2x 32GB 4800MHz DDR5 | No | 2x m.2, 1x 2.5" | |
| M90q Gen 3 | Alder Lake | Intel Q670 | 2x 32GB 4800MHz DDR5 | PCIe x8 Gen 4 | 2x m.2, 1x 2.5" | |
| P360 | Alder Lake | Intel Q670 | 2x 32GB 4800MHz DDR5 | PCIe x8 Gen 4 | 2x m.2, 1x 2.5" | |
| M70q Gen 3 | Alder Lake | Intel Q670 | 2x 32GB 3200MHz DDR4 | No | 2x m.2, 1x 2.5" | |

## Sources

- [Project TinyMiniMicro](https://forums.servethehome.com/index.php?threads/lenovo-thinkcentre-thinkstation-tiny-project-tinyminimicro-reference-thread.34925/)
- [Tiny/Mini/Micro PC experiences](https://forums.servethehome.com/index.php?threads/tiny-mini-micro-pc-experiences.30230/)
- [Wikipedia](https://en.wikipedia.org/wiki/Small_form_factor)
