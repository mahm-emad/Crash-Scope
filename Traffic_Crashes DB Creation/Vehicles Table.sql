USE [Traffic_Crashes]
GO

/****** Object:  Table [dbo].[Vehicles]    Script Date: 4/24/2025 3:33:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Vehicles](
	[Crash_Unit_ID] [int] IDENTITY(1838271,1) NOT NULL,
	[CRASH_RECORD_ID] [nvarchar](255) NOT NULL,
	[CRASH_DATE] [datetime] NULL,
	[Unit_No] [int] NULL,
	[Unit_Type] [nvarchar](50) NULL,
	[VEHICLE_ID] [int] NULL,
	[Make] [nvarchar](100) NULL,
	[Model] [nvarchar](100) NULL,
	[Lic_Plate_State] [nvarchar](50) NULL,
	[Vehicle_Year] [int] NULL,
	[Vehicle_Defect] [nvarchar](50) NULL,
	[Vehicle_Type] [nvarchar](100) NULL,
	[Vehicle_Use] [nvarchar](100) NULL,
	[Travel_direction] [nvarchar](50) NULL,
	[maneuver] [nvarchar](100) NULL,
	[Occupant_CNT] [int] NULL,
	[First_contact_point] [nvarchar](100) NULL,
 CONSTRAINT [PK_Vehicles] PRIMARY KEY CLUSTERED 
(
	[Crash_Unit_ID] ASC,
	[CRASH_RECORD_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Vehicles] ADD  CONSTRAINT [DF__Vehicles__CRASH___398D8EEE]  DEFAULT (getdate()) FOR [CRASH_DATE]
GO

ALTER TABLE [dbo].[Vehicles]  WITH CHECK ADD  CONSTRAINT [FK_Vehicles_Crashes] FOREIGN KEY([CRASH_RECORD_ID])
REFERENCES [dbo].[Crashes] ([CRASH_RECORD_ID])
GO

ALTER TABLE [dbo].[Vehicles] CHECK CONSTRAINT [FK_Vehicles_Crashes]
GO


