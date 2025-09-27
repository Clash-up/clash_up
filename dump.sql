--
-- PostgreSQL database dump
--

\restrict WDHgMgpf03bTh8CtLQaw0iNMr6FzeiHN7JkF1YRb6IUOUzgOae7TA5GW11L4uNZ

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: role; Type: TYPE; Schema: public; Owner: clash_up
--

CREATE TYPE public.role AS ENUM (
    'NOT_MEMBER',
    'MEMBER',
    'LEADER',
    'ELDER',
    'COLEADER'
);


ALTER TYPE public.role OWNER TO clash_up;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: player; Type: TABLE; Schema: public; Owner: clash_up
--

CREATE TABLE public.player (
    name character varying(50) NOT NULL,
    tag character varying(20) NOT NULL,
    trophies integer NOT NULL,
    donations integer NOT NULL,
    donations_received integer NOT NULL,
    role public.role NOT NULL,
    town_hall_level integer NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.player OWNER TO clash_up;

--
-- Name: war_entry; Type: TABLE; Schema: public; Owner: clash_up
--

CREATE TABLE public.war_entry (
    war_id uuid NOT NULL,
    stars integer,
    destruction_percentage integer,
    duration integer,
    player_id uuid NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.war_entry OWNER TO clash_up;

--
-- Data for Name: player; Type: TABLE DATA; Schema: public; Owner: clash_up
--

COPY public.player (name, tag, trophies, donations, donations_received, role, town_hall_level, id) FROM stdin;
Dulnik	#9VQ2G29C9	2696	9804	2767	LEADER	13	6d23b747-2dd1-4b0a-8198-335a262dec1e
Zaba	#QLRGGQYJQ	3790	4791	1734	COLEADER	12	e88bd186-2b04-4104-b191-8e282096cc2f
st0rm2	#GYG0GU0UP	2335	1096	1420	ELDER	11	5ead76cf-6d2f-434e-a266-6ac74a7f86fe
sany	#L0GUURU8Q	2033	0	0	MEMBER	13	8a0aa766-65f4-49d2-a6a9-070338d88c59
messi	#YJQJJPG2J	2080	42	131	MEMBER	11	23147b25-b55e-47ba-ad84-21399c24cb62
obi	#QJQ2GYC9V	2195	407	1947	ELDER	12	3c748ece-f2ab-4932-a6f9-ce52238a400b
nadare	#G9CLU2R90	2289	1	67	MEMBER	11	fb95b203-aae2-4024-847a-49d58e074a21
hacker	#YUV89LCLQ	1709	0	0	MEMBER	12	c27ce9af-b980-4cc1-844d-ad45d3002c83
Fooli	#Y9QGRJYR0	3161	4316	4209	COLEADER	14	029e6ea8-37b9-4329-83bb-f1d824bcbede
Crazy&boy	#LG8UYL92C	2568	1528	232	ELDER	12	2591f04b-c0cf-40b3-9910-2071cbc7c7bd
spacerniak	#QP88V9JGJ	2336	1603	1514	COLEADER	11	d9412d94-9f0f-4181-b9c4-62dba6be5bdc
Price A R M	#QQCJ9QCU0	2141	0	0	MEMBER	11	a1ad6b73-511e-415c-9163-7da905b1423c
zeev	#Q2Y922LY9	1689	0	35	MEMBER	11	5f0d1b67-6b26-4597-a9ce-1f6ea6e66a0a
tinapie	#YV2CY2RP	1669	0	67	MEMBER	11	166e6ab8-064b-4de0-92ba-17a55162bb7a
dragonslayer	#QLCGGGV22	3211	5285	1613	ELDER	12	a607b57f-2f3c-4b4f-b1dc-47c58e8eb9a1
chitmgmg	#GCG9PGCJ9	1698	6	0	MEMBER	11	216f976a-e346-44d0-9511-7255bb171350
Jack	#GUUPUCYY8	2837	42	167	MEMBER	11	e42184e0-4e04-41aa-bd25-df560e3a8666
BigiLoka	#GUQUG0VJ8	1661	0	0	MEMBER	11	b6100652-538f-498e-b705-e3b5e91a331c
4nv4r	#P9YUP982Y	1530	0	0	MEMBER	11	e0f448cb-3d41-4f0a-9d0e-550a3adc135b
Raghav	#Q8JQPLP02	2375	333	976	ELDER	11	ae7dcf11-7e42-4cb2-ba46-ad0f6d1aa7ac
sunny	#9JYCJUR08	1701	0	193	MEMBER	11	862523fd-a706-4110-9f2e-60435cd6750b
duckybucky2637	#GRR8CL0V2	966	222	186	MEMBER	11	e941703c-bbb1-4280-894a-b5df1da747b5
Kristof	#PVLQ0C2QR	1366	37	152	MEMBER	11	b2e75ec2-d16f-4eef-a56c-027ee6d2cd6f
Anka	#GUPR89JPQ	693	4	35	MEMBER	6	14018683-d3f3-4b88-85b6-aa4ac7077c78
KweePhyo	#GJ828PJ8C	2177	0	66	MEMBER	11	a0c81bbd-e794-4088-822c-8cbcae64790e
yhaybi	#GC2U28UPP	1259	0	0	MEMBER	11	e0e3c991-7653-4d32-bf48-3f7fbe0620eb
Clousify	#QLC2LVJ9Y	1070	72	102	MEMBER	11	cf24bf95-8c41-421e-be45-90efc0f3fb32
Николай	#QGPJ0LJCJ	1427	1	51	MEMBER	11	96b66348-b0d2-4395-be26-8a5e1b2b91f4
king	#R0888GLR9	1167	0	0	MEMBER	11	c5031065-1aa2-4928-b6f4-5f73ad9d922c
Nehal	#GCRUGVQUC	1290	0	31	MEMBER	12	6682f62f-cfdb-495c-93cd-a488fe19ebbe
mm	#GCJ2UVYPR	856	1	150	ELDER	7	ae4f882d-0429-495b-83df-f8a849a26505
Arafat ali	#QGQQ8V2P0	1027	0	0	MEMBER	11	85af26ab-65b0-40f9-9d47-87dde7492311
boss	#QRCPVQPRP	1564	25	73	MEMBER	11	af5e3fed-b78a-46c0-9058-ceee6c698109
JETHROCK	#GL2YU0GUU	1583	0	0	MEMBER	11	87efe845-2e51-4c94-a8ae-e3c67c4f1f2c
DynamoKing	#PY2PG2GU9	1109	0	0	MEMBER	11	b4d44ebd-6827-4015-8dcf-83f0b2dc0bc2
mati_cbr	#GGQC2PV2L	1534	389	2790	ELDER	9	ac01f559-7c6e-4518-8380-0f1977957fd0
mumbai	#GRPUL22GG	2065	568	860	MEMBER	11	9825868d-6ca1-487c-93df-a83453b6ead6
maons.-	#QJ8P0Q8GU	1502	605	284	MEMBER	12	03cf47bc-cf19-4068-b193-ce74de5b1487
KYLL	#GRG8JL090	1386	31	0	MEMBER	11	25788104-355a-419a-a4a3-46722221f604
ZERRY	#GJ89GVVYG	845	11	156	MEMBER	9	a35dabe0-1e99-4236-99ac-b86f2a76422c
\.


--
-- Data for Name: war_entry; Type: TABLE DATA; Schema: public; Owner: clash_up
--

COPY public.war_entry (war_id, stars, destruction_percentage, duration, player_id, id) FROM stdin;
\.


--
-- Name: player player_pkey; Type: CONSTRAINT; Schema: public; Owner: clash_up
--

ALTER TABLE ONLY public.player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- Name: war_entry war_entry_pkey; Type: CONSTRAINT; Schema: public; Owner: clash_up
--

ALTER TABLE ONLY public.war_entry
    ADD CONSTRAINT war_entry_pkey PRIMARY KEY (id);


--
-- Name: ix_player_tag; Type: INDEX; Schema: public; Owner: clash_up
--

CREATE UNIQUE INDEX ix_player_tag ON public.player USING btree (tag);


--
-- Name: ix_war_entry_war_id; Type: INDEX; Schema: public; Owner: clash_up
--

CREATE INDEX ix_war_entry_war_id ON public.war_entry USING btree (war_id);


--
-- Name: war_entry war_entry_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clash_up
--

ALTER TABLE ONLY public.war_entry
    ADD CONSTRAINT war_entry_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.player(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict WDHgMgpf03bTh8CtLQaw0iNMr6FzeiHN7JkF1YRb6IUOUzgOae7TA5GW11L4uNZ

