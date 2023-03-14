program bufr_decode_g16

    implicit none

    integer(8), parameter :: i_long = selected_int_kind(8)
    integer(8), parameter :: r_double = selected_real_kind(15)
    
    character(150) :: headerstr  = 'SAID SIID OGCE GSES'
    character(150) :: yymmddstr  = 'YEAR MNTH DAYS'
    character(150) :: hhmmssstr  = 'HOUR MINU SECW'
    character(150) :: l2bgeostr  = 'CRDSIG CLATH CLONH TISE HEITH BEARAZ ELEV SATRG'
    character(150) :: l2binfostr = 'PFNUM OBSID RCVCH LL2BCT HOIL HLSW HLSWEE CONFLG'
    character(150) :: l2bptbstr  = 'PRES TMDBST BKSTR DWPRS DWTMP DWBR'
    character(8)   :: subset

    real(r_double), dimension(4)   :: header
    real(r_double), dimension(3)   :: yymmdd
    real(r_double), dimension(3)   :: hhmmss
    real(r_double), dimension(8,6) :: l2bgeo
    real(r_double), dimension(8)   :: l2binfo
    real(r_double), dimension(6)   :: l2bptb

    integer :: unit_in = 10, unit_table = 24
    integer :: ireadmg, ireadsb
    integer :: idate, nmsg, ntb
    integer :: i, iret

    open(unit_in, file='gdas.aeolus.bufr', form='unformatted', status='old')
    call openbf(unit_in,'IN',unit_in)
    call dxdump(unit_in,unit_table)
    call datelen(10)

    nmsg = 0
    ntb = 0
    msg_report: do while (ireadmg(unit_in, subset, idate) == 0)
        nmsg = nmsg + 1
        write(*,'(3a, i10)') 'subset = ', subset, ' cycle time = ', idate
        sb_report: do while (ireadsb(unit_in) == 0)
            ntb = ntb + 1
            call ufbint(unit_in,  header, 4, 1, iret, trim( headerstr))
            call ufbint(unit_in,  yymmdd, 3, 1, iret, trim( yymmddstr))
            call ufbint(unit_in,  hhmmss, 3, 1, iret, trim( hhmmssstr))
            call ufbrep(unit_in,  l2bgeo, 8, 6, iret, trim( l2bgeostr))
            call ufbint(unit_in, l2binfo, 8, 1, iret, trim(l2binfostr))
            call ufbint(unit_in,  l2bptb, 6, 1, iret, trim( l2bptbstr))
            write(*, *) headerstr
            write(*, '(4f16.4)') header
            write(*, *) yymmddstr
            write(*, '(3f16.4)') yymmdd
            write(*, *) hhmmssstr
            write(*, '(3f16.4)') hhmmss
            write(*, *) l2bgeostr
            do i = 1, 6
                write(*, '(8f16.4)') l2bgeo(:,i)
            end do
            write(*, *) l2binfostr
            write(*, '(8f16.4)') l2binfo
            write(*, *) l2bptbstr
            write(*, '(6f16.4)') l2bptb
        enddo sb_report
    enddo msg_report
    call closbf(unit_in)

end program
