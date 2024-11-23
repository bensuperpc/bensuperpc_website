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

SSP PCs are often in x86 but for several years now, ARM SSP PCs are more and more popular, they are generally cheaper, more power efficient, but have limited software compatibility, upgrade options and performance.

In this guide, we will focus on x86 SSP PCs and Raspberry Pi.

## SSF PCs components

In this section, we will see the components of SSF PCs.

### CPU (Central Processing Unit)

I recommend using socketed CPUs, they are upgradable to more powerfull CPU, you can for example upgrade from **intel celeron G4900T** to **intel i9 9900T** without any issue in most cases.

| Brand | CPU arch | CPU Gen | Socket | RAM Type | Max RAM | Year | Exemple of SSF PC | Remarks |
|-------|----------|--------|--------|----------|---------|------|----------------| ------- |
| intel | Nehalem | 1st Gen | LGA1156 | DDR3 | 16GB | 2008-2009 | | Avoid it, lack of AVX and not very power efficient |
| intel | Sandy Bridge | 2nd Gen | LGA1155 | DDR3 | 32GB | 2011-2012 | | |
| intel | Ivy Bridge | 3rd Gen | LGA1155 | DDR3 | 32GB | 2012-2013 | | |
| intel | Haswell | 4th Gen | LGA1150 | DDR3 | 32GB | 2013-2014 | M73 tiny | Good choice and support AVX2 |
| intel | Broadwell | 5th Gen | LGA1150 | DDR3 | 32GB | 2014-2015 | | |
| intel | Skylake | 6th Gen | LGA1151 | DDR4 | 64GB | 2015-2016 | M710q | |
| intel | Kaby Lake | 7th Gen | LGA1151 | DDR4 | 64GB | 2016-2017 | M710q | HEVC/VP9 10-bit hardware decoding support |
| intel | Coffee Lake | 8-9th Gen | LGA1151 | DDR4 | 64GB | 2017-2018 | M720q | |
| intel | Comet Lake | 10th Gen | LGA1200 | DDR4 | 128GB | 2020-2021 | M70G gen 1 | |
| intel | Rocket Lake | 11th Gen | LGA1200 | DDR4 | 128GB | 2021-2022 | M70G gen 2 | |
| intel | Alder Lake | 12th Gen | LGA1700 | DDR5 | 128GB | 2021-2022 | M70G gen 3 | |
| intel | Raptor Lake | 13-14th Gen | LGA1700 | DDR5 | 128GB | 2022-2023 | M70G gen 4 | |
| AMD | Zen | 1st Gen | AM4 | DDR4 | 64GB | 2017-2018 | | |
| AMD | Zen+ | 2nd Gen | AM4 | DDR4 | 64GB | 2018-2019 | | |
| AMD | Zen 2 | 3rd Gen | AM4 | DDR4 | 128GB | 2019-2020 | | |
| AMD | Zen 3 | 4th Gen | AM4 | DDR4 | 128GB | 2020-2021 | | |
| AMD | Zen 4 | 5th Gen | AM5 | DDR5 | 128GB | 2021-2022 | | |
| AMD | Zen 5 | 6th Gen | AM5 | DDR5 | 128GB | 2022-2023 | | |

### GPU (Graphics Processing Unit)

Most SSF PCs have only integrated GPU, they are generally enough for light GPU tasks and consume very low power, great for home servers or office PCs.

Some SSF PCs (can) have a dedicated GPU (Like the M720Q), they are mostly in low profile, it can be useful for light gaming, video editing, etc...

### RAM (Random Access Memory)

For SSF PCs, you generally have 2 RAM slots, you can use DDR3, DDR4 RAM or DDR5 RAM, the maximum capacity is generally 16GB to 128GB depending on motherboard and CPU.

### Storage

SSF PCs have 4 storage options (depending on the model):

- **M.2 NVMe SSD**: They are very fast and they are present in most SSF PCs* (since 2015), the optimal choice.
- **M.2 SATA SSD**: Use same connector as NVMe but slower with SATA interface (In thinkcentre M700 for example).
- **2.5" SATA SSD**: They are slower than M.2 SSD but it's a good choice if you can't use M.2 SSD.
- **2.5" SATA HDD**: They are very slow and generally not recommended, but they can be easily replaced by SSD.
- **On board eMMC**: On motherboard memory, **you should avoid it**, it's generally slow, limited and once it's dead, you must replace the motherboard.

I recommend using **M.2 NVMe SSDs**, beware of the size (2242, 2260, 2280), the key (B, M, B+M) and simple or double sided.

### PSU (Power Supply Unit)

Most SSF PCs have an external power supply, often have a proprietary connector.

### Ports

### Motherboard

## Sources

- [Project TinyMiniMicro](https://forums.servethehome.com/index.php?threads/lenovo-thinkcentre-thinkstation-tiny-project-tinyminimicro-reference-thread.34925/)
- [Tiny/Mini/Micro PC experiences](https://forums.servethehome.com/index.php?threads/tiny-mini-micro-pc-experiences.30230/)
- [Wikipedia](https://en.wikipedia.org/wiki/Small_form_factor)
