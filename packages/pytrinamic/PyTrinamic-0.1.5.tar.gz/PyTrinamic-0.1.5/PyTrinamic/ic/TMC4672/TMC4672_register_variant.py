'''
Created on 15.02.2019

@author: ed
'''

class TMC4672_register_variant:

    " ===== TMC4672 register variants ===== "

    CHIPINFO_ADDR_SI_TYPE                                   = 0
    CHIPINFO_ADDR_SI_VERSION                                = 1
    CHIPINFO_ADDR_SI_DATA                                   = 2
    CHIPINFO_ADDR_SI_TIME                                   = 3
    CHIPINFO_ADDR_SI_VARIANT                                = 4
    CHIPINFO_ADDR_SI_BUILD                                  = 5

    ADC_RAW_ADDR_ADC_I1_I0_RAW                              = 0
    ADC_RAW_ADDR_ADC_AGPI_A_ADC_VM_RAW                      = 1
    ADC_RAW_ADDR_ADC_AENC_WY_UX_RAW                         = 2
    ADC_RAW_ADDR_ADC_AGPI_B_AENC_VN_RAW                     = 3

    ADC_CONFIG_ADDR_dsADC_MCFG_B_MCFG_A                     = 0
    ADC_CONFIG_ADDR_dsADC_MCLK_B_MCLK_A                     = 1
    ADC_CONFIG_ADDR_dsADC_MDEC_B_MDEC_A                     = 2
    ADC_CONFIG_ADDR_DS_INPUT_STAGE_PAD_MODE                 = 3
    ADC_CONFIG_ADDR_DS_INPUT_STAGE_GAIN_SnH                 = 4
    ADC_CONFIG_ADDR_DS_SnH_PULSE_LENGTH_B_A                 = 5
    ADC_CONFIG_ADDR_ADC_I_SELECT                            = 6
    ADC_CONFIG_ADDR_ADC_I0_SCALE_OFFSET                     = 7
    ADC_CONFIG_ADDR_ADC_I1_SCALE_OFFSET                     = 8
    ADC_CONFIG_ADDR_ADC_I2_SCALE_OFFSET                     = 9
    ADC_CONFIG_ADDR_ADC_I3_SCALE_OFFSET                     = 10
    ADC_CONFIG_ADDR_PWM_SWITCH_LIMIT                        = 11
    ADC_CONFIG_ADDR_ADC_VM_SELECT                           = 12
    ADC_CONFIG_ADDR_AENC_SELECT                             = 13
    ADC_CONFIG_ADDR_AENC_UX_SCALE_OFFSET                    = 14
    ADC_CONFIG_ADDR_AENC_VN_SCALE_OFFSET                    = 15
    ADC_CONFIG_ADDR_AENC_WY_SCALE_OFFSET                    = 16

    DECODER_CONFIG_ADDR_ABN_DECODER_MODE                    = 0
    DECODER_CONFIG_ADDR_ABN_DECODER_PPR                     = 1
    DECODER_CONFIG_ADDR_ABN_DECODER_PHI_E_PHI_M_OFFSET      = 2
    DECODER_CONFIG_ADDR_ABN_DECODER_ERROR_AMPL_ERROR_PHASE  = 3
    DECODER_CONFIG_ADDR_ABN_2_DECODER_MODE                  = 4
    DECODER_CONFIG_ADDR_ABN_2_DECODER_PPR                   = 5
    DECODER_CONFIG_ADDR_ABN_2_DECODER_PHI_E_PHI_M_OFFSET    = 6
    DECODER_CONFIG_ADDR_HALL_MODE                           = 7
    DECODER_CONFIG_ADDR_HALL_POSITION_060_000               = 8
    DECODER_CONFIG_ADDR_HALL_POSITION_180_120               = 9
    DECODER_CONFIG_ADDR_HALL_POSITION_300_240               = 10
    DECODER_CONFIG_ADDR_HALL_PHI_E_PHI_M_OFFSET             = 11
    DECODER_CONFIG_ADDR_HALL_DPHI_MAX                       = 12
    DECODER_CONFIG_ADDR_AENC_MODE                           = 13
    DECODER_CONFIG_ADDR_AENC_N_THRESHOLD_N_PULSE_POLARITY   = 14
    DECODER_CONFIG_ADDR_AENC_PPR                            = 15
    DECODER_CONFIG_ADDR_AENC_PHI_E_PHI_M_OFFSET             = 16
    DECODER_CONFIG_ADDR_SPI_MASTER_STATUS                   = 17
    DECODER_CONFIG_ADDR_SPI_GEN_CONFIG_REG                  = 18
    DECODER_CONFIG_ADDR_SPI_SCLK_CONFIG_REG                 = 19
    DECODER_CONFIG_ADDR_SPI_SYNC_CONFIG_REG                 = 20
    DECODER_CONFIG_ADDR_SPI_ENC_MASK_HW                     = 21
    DECODER_CONFIG_ADDR_SPI_ENC_MASK_LW                     = 22
    DECODER_CONFIG_ADDR_SPI_ENC_SHIFT                       = 23
    DECODER_CONFIG_ADDR_SPI_CAP_COMP_VAL_HW                 = 24
    DECODER_CONFIG_ADDR_SPI_CAP_COMP_VAL_LW                 = 25
    DECODER_CONFIG_ADDR_SPI_WR_BUFF_0                       = 26
    DECODER_CONFIG_ADDR_SPI_WR_BUFF_1                       = 27
    DECODER_CONFIG_ADDR_SPI_WR_BUFF_2                       = 28
    DECODER_CONFIG_ADDR_SPI_WR_BUFF_3                       = 29
    DECODER_CONFIG_ADDR_SPI_RD_BUFF_0                       = 30
    DECODER_CONFIG_ADDR_SPI_RD_BUFF_1                       = 31
    DECODER_CONFIG_ADDR_SPI_RD_BUFF_2                       = 32
    DECODER_CONFIG_ADDR_SPI_RD_BUFF_3                       = 33
    DECODER_CONFIG_ADDR_SPI_ENCODER_PHI_E_PHI_M_OFFSET      = 34
    DECODER_CONFIG_ADDR_SPI_ENCODER_ERROR_AMPL_ERROR_PHASE  = 35

    CONFIG_ADDR_BIQUAD_X_A_1                                = 1
    CONFIG_ADDR_BIQUAD_X_A_2                                = 2
    CONFIG_ADDR_BIQUAD_X_B_0                                = 4
    CONFIG_ADDR_BIQUAD_X_B_1                                = 5
    CONFIG_ADDR_BIQUAD_X_B_2                                = 6
    CONFIG_ADDR_BIQUAD_X_ENABLE                             = 7
    CONFIG_ADDR_BIQUAD_V_A_1                                = 9
    CONFIG_ADDR_BIQUAD_V_A_2                                = 10
    CONFIG_ADDR_BIQUAD_V_B_0                                = 12
    CONFIG_ADDR_BIQUAD_V_B_1                                = 13
    CONFIG_ADDR_BIQUAD_V_B_2                                = 14
    CONFIG_ADDR_BIQUAD_V_ENABLE                             = 15
    CONFIG_ADDR_BIQUAD_T_A_1                                = 17
    CONFIG_ADDR_BIQUAD_T_A_2                                = 18
    CONFIG_ADDR_BIQUAD_T_B_0                                = 20
    CONFIG_ADDR_BIQUAD_T_B_1                                = 21
    CONFIG_ADDR_BIQUAD_T_B_2                                = 22
    CONFIG_ADDR_BIQUAD_T_ENABLE                             = 23
    CONFIG_ADDR_BIQUAD_F_A_1                                = 25
    CONFIG_ADDR_BIQUAD_F_A_2                                = 26
    CONFIG_ADDR_BIQUAD_F_B_0                                = 28
    CONFIG_ADDR_BIQUAD_F_B_1                                = 29
    CONFIG_ADDR_BIQUAD_F_B_2                                = 30
    CONFIG_ADDR_BIQUAD_F_ENABLE                             = 31
    CONFIG_ADDR_PRBS_AMPLITUDE                              = 32
    CONFIG_ADDR_PRBS_DOWN_SAMPLING_RATIO                    = 33
    CONFIG_ADDR_PWM_IRQ_CFG                                 = 34
    CONFIG_ADDR_MAX_POS_DEVIATION                           = 39
    CONFIG_ADDR_FEED_FORWARD_VELOCITY_GAIN                  = 40
    CONFIG_ADDR_FEED_FORWARD_VELICITY_FILTER_CONSTANT       = 41
    CONFIG_ADDR_FEED_FORWARD_TORQUE_GAIN                    = 42
    CONFIG_ADDR_FEED_FORWARD_TORGUE_FILTER_CONSTANT         = 43
    CONFIG_ADDR_REF_SWITCH_CONFIG                           = 51
    CONFIG_ADDR_ENABLE_ENCODER_INIT_HALL                    = 52
    CONFIG_ADDR_DIG_FILTER_CFG                              = 53
    CONFIG_ADDR_SINGLE_PIN_IF_CFG                           = 54
    CONFIG_ADDR_SINGLE_PIN_IF_SCALE_OFFSET                  = 55
    CONFIG_ADDR_SINGLE_PIN_IF_DIG_FILTER_CFG                = 56

    PID_ERROR_ADDR_PID_ERROR_PID_TORQUE_ERROR               = 0
    PID_ERROR_ADDR_PID_ERROR_PID_FLUX_ERROR                 = 1
    PID_ERROR_ADDR_PID_ERROR_PID_VELOCITY_ERROR             = 2
    PID_ERROR_ADDR_PID_ERROR_PID_POSITION_ERROR             = 3
    PID_ERROR_ADDR_PID_ERROR_PID_TORQUE_INTEGRATOR          = 4
    PID_ERROR_ADDR_PID_ERROR_PID_FLUX_INTEGRATOR            = 5
    PID_ERROR_ADDR_PID_ERROR_PID_VELOCITY_INTEGRATOR        = 6
    PID_ERROR_ADDR_PID_ERROR_PID_POSITION_INTEGRATOR        = 7

    INTERIM_ADDR_INTERIM_PIDIN_TARGET_TORQUE                = 0
    INTERIM_ADDR_INTERIM_PIDIN_TARGET_FLUX                  = 1
    INTERIM_ADDR_INTERIM_PIDIN_TARGET_VELOCITY              = 2
    INTERIM_ADDR_INTERIM_PIDIN_TARGET_POSITION              = 3
    INTERIM_ADDR_INTERIM_PIDOUT_TARGET_TORQUE               = 4
    INTERIM_ADDR_INTERIM_PIDOUT_TARGET_FLUX                 = 5
    INTERIM_ADDR_INTERIM_PIDOUT_TARGET_VELOCITY             = 6
    INTERIM_ADDR_INTERIM_PIDOUT_TARGET_POSITION             = 7
    INTERIM_ADDR_INTERIM_FOC_IWY_IUX                        = 8
    INTERIM_ADDR_INTERIM_FOC_IV                             = 9
    INTERIM_ADDR_INTERIM_FOC_IB_IA                          = 10
    INTERIM_ADDR_INTERIM_FOC_IQ_ID                          = 11
    INTERIM_ADDR_INTERIM_FOC_UQ_UD                          = 12
    INTERIM_ADDR_INTERIM_FOC_UQ_UD_LIMITED                  = 13
    INTERIM_ADDR_INTERIM_FOC_UB_UA                          = 14
    INTERIM_ADDR_INTERIM_FOC_UWY_UUX                        = 15
    INTERIM_ADDR_INTERIM_FOC_UV                             = 16
    INTERIM_ADDR_INTERIM_PWM_WY_UX                          = 17
    INTERIM_ADDR_INTERIM_PWM_UV                             = 18
    INTERIM_ADDR_INTERIM_ADC_I1_I0                          = 19
    INTERIM_ADDR_INTERIM_ADC_I3_I2                          = 20
    INTERIM_ADDR_PID_TORQUE_TARGET_TORQUE_ACTUAL            = 21
    INTERIM_ADDR_PID_FLUX_TARGET_FLUX_ACTUAL                = 22
    INTERIM_ADDR_PID_VELOCITY_TARGET_VELOCITY_ACTUAL_DIV256 = 23
    INTERIM_ADDR_PID_VELOCITY_TARGET_VELOCITY_ACTUAL        = 24
    INTERIM_ADDR_PID_POSITION_TARGET_POSITION_ACTUAL_DIV256 = 25
    INTERIM_ADDR_PID_POSITION_TARGET_POSITION_ACTUAL        = 26
    INTERIM_ADDR_FF_VELOCITY                                = 27
    INTERIM_ADDR_FF_TORQUE                                  = 28
    INTERIM_ADDR_REF_SWITCH_STATUS                          = 30
    INTERIM_ADDR_HOME_POSITION                              = 31
    INTERIM_ADDR_LEFT_POSITION                              = 32
    INTERIM_ADDR_RIGHT_POSITION                             = 33
    INTERIM_ADDR_ENC_INIT_HALL_STATUS                       = 34
    INTERIM_ADDR_ENC_INIT_HALL_PHI_E_ABN_OFFSET             = 35
    INTERIM_ADDR_ENC_INIT_HALL_PHI_E_AENC_OFFSET            = 36
    INTERIM_ADDR_ENC_INIT_HALL_PHI_A_AENC_OFFSET            = 37
    INTERIM_ADDR_SINGLE_PIN_IF_PWM_DUTY_CYCLE_INPUT_RAW     = 38
    INTERIM_ADDR_SINGLE_PIN_IF_TORQUE_TARGET                = 39
    INTERIM_ADDR_SINGLE_PIN_IF_VELOCITY_TARGET              = 40
    INTERIM_ADDR_SINGLE_PIN_IF_POSITION_TARGET              = 41
    INTERIM_ADDR_ABN_DECODER_PHI_M_RAW                      = 42
    INTERIM_ADDR_SPI_ENCODER_PHI_M_RAW                      = 43
    INTERIM_ADDR_INTERIM_DEBUG_1_0                          = 192
    INTERIM_ADDR_INTERIM_DEBUG_3_2                          = 193
    INTERIM_ADDR_INTERIM_DEBUG_5_4                          = 194
    INTERIM_ADDR_INTERIM_DEBUG_7_6                          = 195
    INTERIM_ADDR_INTERIM_DEBUG_9_8                          = 196
    INTERIM_ADDR_INTERIM_DEBUG_B_A                          = 197
    INTERIM_ADDR_INTERIM_DEBUG_D_C                          = 198
    INTERIM_ADDR_INTERIM_DEBUG_F_E                          = 199
    INTERIM_ADDR_INTERIM_DEBUG_16                           = 200
    INTERIM_ADDR_INTERIM_DEBUG_17                           = 201
    INTERIM_ADDR_INTERIM_DEBUG_18                           = 202
    INTERIM_ADDR_INTERIM_DEBUG_19                           = 203
