program bufr_encode_g16

    implicit none

    integer(8), parameter :: i_long = selected_int_kind(8)
    integer(8), parameter :: r_double = selected_real_kind(15)
    integer(8), parameter :: npara = 51

    character(150) :: dir_files
    character(200) :: file_name
    character(150) :: msgtype
    character(150) :: strdate

    character(150) :: headerstr  = 'SAID SIID OGCE GSES'
    character(150) :: yymmddstr  = 'YEAR MNTH DAYS'
    character(150) :: hhmmssstr  = 'HOUR MINU SECW'
    character(150) :: l2bgeostr  = 'CRDSIG CLATH CLONH TISE HEITH BEARAZ ELEV SATRG'
    character(150) :: l2binfostr = 'PFNUM OBSID RCVCH LL2BCT HOIL HLSW HLSWEE CONFLG'
    character(150) :: l2bptbstr  = 'PRES TMDBST BKSTR DWPRS DWTMP DWBR'

    real(r_double), dimension(4)   :: header
    real(r_double), dimension(3)   :: yymmdd
    real(r_double), dimension(3)   :: hhmmss
    real(r_double), dimension(8,6) :: l2bgeo
    real(r_double), dimension(8)   :: l2binfo
    real(r_double), dimension(6)   :: l2bptb
    real(r_double), allocatable, dimension(:,:) :: datainput

    integer(i_long) :: unit_file, unit_table, lnbufr
    integer(i_long) :: idate, ndata
    integer(i_long) :: iret, error
    integer(i_long) :: I, J

    !YYYYMMDDHH
    idate = 2021082600
    write(strdate, '(I10)') idate
    write(*,*) idate

    dir_files = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/Aeolus/create_bufr/bufr_temp/'
    dir_files = trim(dir_files) // trim(strdate)
    dir_files = trim(dir_files) // '/'
    file_name = trim(dir_files) // '0.txt'
    unit_file = 10
    open(unit_file, file=file_name, status='old', iostat=error)
    read(unit_file, fmt=*, iostat=error) ndata
    close(unit_file)
    write(*,*) 'ndata = ', ndata
    allocate(datainput(npara, ndata))

    DO I = 1, npara
        write(file_name, *) I
        file_name = trim(dir_files) // adjustl(file_name)
        file_name = trim(file_name) // '.txt'
        open(unit_file, file=file_name, status='old', iostat=error)
        DO J = 1, ndata
            read(unit_file, fmt=*, iostat=error) datainput(I, J)
        END DO
        close(unit_file)
    END DO

    !Aeolus L2B message type
    msgtype = 'ALADIN2B'

    unit_table = 24
    lnbufr = 10

    !Open radiance bufrtable
    open(unit_table, file='L2B.bufrtable')
    open(lnbufr, file='gdas.aeolus.bufr', action='write', form='unformatted', status='new')
    !specify date format: YYYYMMDDHH
    call datelen(10)
    !Connect bufrtable, bufr file to bufr lib
    call openbf(lnbufr, 'OUT', unit_table)
    !Open the new message type
    call openmb(lnbufr, msgtype, idate)

    DO I = 1, ndata

        header(1) = datainput( 1, I)
        header(2) = datainput( 2, I)
        header(3) = datainput( 3, I)
        header(4) = datainput( 4, I)
        yymmdd(1) = datainput( 5, I)
        yymmdd(2) = datainput( 6, I)
        yymmdd(3) = datainput( 7, I)
        hhmmss(1) = datainput( 8, I)
        hhmmss(2) = datainput( 9, I)
        hhmmss(3) = datainput(10, I)
        l2bgeo(1, 1) = datainput(11, I)
        l2bgeo(2, 1) = datainput(12, I)
        l2bgeo(3, 1) = datainput(13, I)
        l2bgeo(4, 1) = datainput(14, I)
        l2bgeo(1, 2) = datainput(15, I)
        l2bgeo(2, 2) = datainput(16, I)
        l2bgeo(3, 2) = datainput(17, I)
        l2bgeo(4, 2) = datainput(18, I)
        l2bgeo(1, 3) = datainput(19, I)
        l2bgeo(2, 3) = datainput(20, I)
        l2bgeo(3, 3) = datainput(21, I)
        l2bgeo(4, 3) = datainput(22, I)
        l2bgeo(1, 4) = datainput(23, I)
        l2bgeo(5, 4) = datainput(24, I)
        l2bgeo(6, 4) = datainput(25, I)
        l2bgeo(7, 4) = datainput(26, I)
        l2bgeo(8, 4) = datainput(27, I)
        l2bgeo(1, 5) = datainput(28, I)
        l2bgeo(5, 5) = datainput(29, I)
        l2bgeo(6, 5) = datainput(30, I)
        l2bgeo(7, 5) = datainput(31, I)
        l2bgeo(8, 5) = datainput(32, I)
        l2bgeo(1, 6) = datainput(33, I)
        l2bgeo(5, 6) = datainput(34, I)
        l2bgeo(6, 6) = datainput(35, I)
        l2bgeo(7, 6) = datainput(36, I)
        l2bgeo(8, 6) = datainput(37, I)
        l2binfo(1) = datainput(38, I)
        l2binfo(2) = datainput(39, I)
        l2binfo(3) = datainput(40, I)
        l2binfo(4) = datainput(41, I)
        l2binfo(5) = datainput(42, I)
        l2binfo(6) = datainput(43, I)
        l2binfo(7) = datainput(44, I)
        l2binfo(8) = datainput(45, I)
        l2bptb(1)  = datainput(46, I)
        l2bptb(2)  = datainput(47, I)
        l2bptb(3)  = datainput(48, I)
        l2bptb(4)  = datainput(49, I)
        l2bptb(5)  = datainput(50, I)
        l2bptb(6)  = datainput(51, I)

        call ufbint(lnbufr,  header, 4, 1, iret, trim( headerstr)) 
        call ufbint(lnbufr,  yymmdd, 3, 1, iret, trim( yymmddstr)) 
        call ufbint(lnbufr,  hhmmss, 3, 1, iret, trim( hhmmssstr)) 
        call ufbrep(lnbufr,  l2bgeo, 8, 6, iret, trim( l2bgeostr))
        call ufbint(lnbufr, l2binfo, 8, 1, iret, trim(l2binfostr)) 
        call ufbint(lnbufr,  l2bptb, 6, 1, iret, trim( l2bptbstr)) 

        !write the above data subset to the current message type.
        call writsb(lnbufr)

    ENDDO

    call closmg(lnbufr)
    call closbf(lnbufr)
    deallocate(datainput)

end program
