# Linux-debug
1.Установка bcc на host систему.
Подробные инструкции для разных дистрибутивов:
  https://github.com/iovisor/bcc/blob/master/INSTALL.md#older-instructions
  Установка qemu.
  sudo apt install qemu
2.Создание моста на хост системе:
  ip link add br0 type bridge
  ifconfig br0 up
  (Мосту будет автоматически выдан ipv6 адресс)
3.Конфигурация и сборка ядра.
	3.1.Скачиваем и распаковываем файлы ядра.
  wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.20.4.tar.xz
  tar xf linux-4.20.4.tar.xz
	3.2. Приступим к конфигурауии ядра.
  make defconfig
  make kvmconfig
  Для машины на которой будут установлены инструменты bcc:
  make menucofig (может понадобиться установить дополнительные пакеты, например libncurses5-dev)
  Теперь необходимо установить необходимые флаги:
  CONFIG_BPF=y
  CONFIG_BPF_SYSCALL=y
  CONFIG_NET_CLS_BPF=m
  CONFIG_NET_ACT_BPF=m
  CONFIG_BPF_JIT=y
  CONFIG_HAVE_BPF_JIT=y
  CONFIG_BPF_EVENTS=y
  CONFIG_NET_SCH_SFQ=m
  CONFIG_NET_ACT_POLICE=m
  CONFIG_NET_ACT_GACT=m
  CONFIG_DUMMY=m
  CONFIG_VXLAN=m
4.Создание образа файловой системы для инициализации.
  sudo mkinitramfs -o init.img
5.Создание корневой файловой системы.
  mkdir rootfs
  sudo qemu-img create -f raw rootfs.img 5g
  sudo mkfs.ext3 rootfs.img
  sudo mount -o loop rootfs.img rootfs
  sudo debootstrap --arch amd64 jessie rootfs
  sudo umount rootfs
6.Запускаем виртуальную машину.
Генерируем случайный mac для виртуальной машины.
  printf 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))
Запускаем qemu.
  sudo qemu-system-x86_64 -kernel ./linux-4.19.10/arch/x86_64/boot/bzImage -enable-kvm -cpu host -nographic -append "console=ttyS0 root=/dev/sda rw single" -initrd ./init.img -m 1024 -drive file=./rootfs.img,index=0,media=disk,format=raw -device e1000,netdev=net0,mac=(вставляем сгенерированный mac) -netdev tap,id=net0,script=./qemu-ifup.sh(скрипт из данного репозитория)
После запуска системы настраиваем сеть.
  dhclient enp0s3
Теперь host система и все гостевые системы, запущенный таким образом на компьютере, находятся в одной локальной сети и могут обмениваться пакетами по протоколу IpV6.

После перезагрузки host системы мост необходимо заново создавать.

