PGDMP  ;    #                |            zomato_app_3313    15.6    16.2 I    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16389    zomato_app_3313    DATABASE     z   CREATE DATABASE zomato_app_3313 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF8';
    DROP DATABASE zomato_app_3313;
                zomato_app_3313_user    false            �           0    0    zomato_app_3313    DATABASE PROPERTIES     8   ALTER DATABASE zomato_app_3313 SET "TimeZone" TO 'utc';
                     zomato_app_3313_user    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                zomato_app_3313_user    false            �            1255    16774    update_order_status()    FUNCTION     �  CREATE FUNCTION public.update_order_status() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if the new row's status is 'Pending' and the order time is 20 minutes or more in the past
    IF NEW.status = 'Pending' AND NEW.order_time + INTERVAL '20 minutes' <= CURRENT_TIMESTAMP THEN
        NEW.status := 'Completed'; -- Change status to 'Completed'
    END IF;
    RETURN NEW;
END;
$$;
 ,   DROP FUNCTION public.update_order_status();
       public          zomato_app_3313_user    false    5            �            1255    16775 '   update_order_status_and_delivery_time()    FUNCTION     	  CREATE FUNCTION public.update_order_status_and_delivery_time() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if the new row's status is 'Pending' and the order time is 20 minutes or more in the past
    IF NEW.status = 'Pending' AND NEW.order_time + INTERVAL '20 minutes' <= CURRENT_TIMESTAMP THEN
        NEW.status := 'Completed'; -- Change status to 'Completed'
        NEW.delivery_time := CURRENT_TIMESTAMP; -- Set delivery time to current timestamp
    END IF;
    RETURN NEW;
END;
$$;
 >   DROP FUNCTION public.update_order_status_and_delivery_time();
       public          zomato_app_3313_user    false    5            �            1259    16685    menu    TABLE     �   CREATE TABLE public.menu (
    menu_id integer NOT NULL,
    restaurant_id integer,
    name text NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    is_available boolean DEFAULT true,
    category text
);
    DROP TABLE public.menu;
       public         heap    zomato_app_3313_user    false    5            �            1259    16684    menu_menu_id_seq    SEQUENCE     �   CREATE SEQUENCE public.menu_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.menu_menu_id_seq;
       public          zomato_app_3313_user    false    5    219            �           0    0    menu_menu_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.menu_menu_id_seq OWNED BY public.menu.menu_id;
          public          zomato_app_3313_user    false    218            �            1259    16737    order_details    TABLE     �   CREATE TABLE public.order_details (
    order_detail_id integer NOT NULL,
    order_id integer,
    menu_id integer,
    quantity integer NOT NULL,
    item_price numeric(10,2) NOT NULL
);
 !   DROP TABLE public.order_details;
       public         heap    zomato_app_3313_user    false    5            �            1259    16736 !   order_details_order_detail_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_details_order_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.order_details_order_detail_id_seq;
       public          zomato_app_3313_user    false    225    5            �           0    0 !   order_details_order_detail_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.order_details_order_detail_id_seq OWNED BY public.order_details.order_detail_id;
          public          zomato_app_3313_user    false    224            �            1259    16700    orders    TABLE       CREATE TABLE public.orders (
    order_id integer NOT NULL,
    user_id integer,
    restaurant_id integer,
    order_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    delivery_time timestamp without time zone,
    status text,
    total_price numeric(10,2) NOT NULL
);
    DROP TABLE public.orders;
       public         heap    zomato_app_3313_user    false    5            �            1259    16699    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public          zomato_app_3313_user    false    221    5            �           0    0    orders_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;
          public          zomato_app_3313_user    false    220            �            1259    16720    payments    TABLE     3  CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    order_id integer,
    payment_type text NOT NULL,
    transaction_id text,
    payment_status text NOT NULL,
    amount_paid numeric(10,2) NOT NULL,
    payment_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT payments_payment_status_check CHECK ((payment_status = ANY (ARRAY['successful'::text, 'pending'::text, 'failed'::text]))),
    CONSTRAINT payments_payment_type_check CHECK ((payment_type = ANY (ARRAY['UPI'::text, 'CARD'::text, 'CASH_ON_DELIVERY'::text])))
);
    DROP TABLE public.payments;
       public         heap    zomato_app_3313_user    false    5            �            1259    16719    payments_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.payments_payment_id_seq;
       public          zomato_app_3313_user    false    5    223            �           0    0    payments_payment_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;
          public          zomato_app_3313_user    false    222            �            1259    16670    restaurants    TABLE       CREATE TABLE public.restaurants (
    restaurant_id integer NOT NULL,
    owner_user_id integer,
    name text NOT NULL,
    restaurant_type text,
    location text,
    rating numeric(3,2),
    is_active boolean DEFAULT true,
    contact_number text,
    description text
);
    DROP TABLE public.restaurants;
       public         heap    zomato_app_3313_user    false    5            �            1259    16669    restaurants_restaurant_id_seq    SEQUENCE     �   CREATE SEQUENCE public.restaurants_restaurant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.restaurants_restaurant_id_seq;
       public          zomato_app_3313_user    false    217    5            �           0    0    restaurants_restaurant_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.restaurants_restaurant_id_seq OWNED BY public.restaurants.restaurant_id;
          public          zomato_app_3313_user    false    216            �            1259    16754    reviews    TABLE     ,  CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    user_id integer,
    restaurant_id integer,
    rating integer,
    comment text,
    review_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reviews_rating_check CHECK (((rating >= 0) AND (rating <= 5)))
);
    DROP TABLE public.reviews;
       public         heap    zomato_app_3313_user    false    5            �            1259    16753    reviews_review_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.reviews_review_id_seq;
       public          zomato_app_3313_user    false    227    5            �           0    0    reviews_review_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;
          public          zomato_app_3313_user    false    226            �            1259    16656    users    TABLE     :  CREATE TABLE public.users (
    user_id integer NOT NULL,
    name text NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    phone_number text,
    is_admin boolean DEFAULT false,
    gender text,
    dob date,
    govt_id text,
    bank_details text,
    address text
);
    DROP TABLE public.users;
       public         heap    zomato_app_3313_user    false    5            �            1259    16655    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          zomato_app_3313_user    false    5    215            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          zomato_app_3313_user    false    214            �           2604    16688    menu menu_id    DEFAULT     l   ALTER TABLE ONLY public.menu ALTER COLUMN menu_id SET DEFAULT nextval('public.menu_menu_id_seq'::regclass);
 ;   ALTER TABLE public.menu ALTER COLUMN menu_id DROP DEFAULT;
       public          zomato_app_3313_user    false    219    218    219            �           2604    16740    order_details order_detail_id    DEFAULT     �   ALTER TABLE ONLY public.order_details ALTER COLUMN order_detail_id SET DEFAULT nextval('public.order_details_order_detail_id_seq'::regclass);
 L   ALTER TABLE public.order_details ALTER COLUMN order_detail_id DROP DEFAULT;
       public          zomato_app_3313_user    false    225    224    225            �           2604    16703    orders order_id    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN order_id DROP DEFAULT;
       public          zomato_app_3313_user    false    220    221    221            �           2604    16723    payments payment_id    DEFAULT     z   ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);
 B   ALTER TABLE public.payments ALTER COLUMN payment_id DROP DEFAULT;
       public          zomato_app_3313_user    false    223    222    223            �           2604    16673    restaurants restaurant_id    DEFAULT     �   ALTER TABLE ONLY public.restaurants ALTER COLUMN restaurant_id SET DEFAULT nextval('public.restaurants_restaurant_id_seq'::regclass);
 H   ALTER TABLE public.restaurants ALTER COLUMN restaurant_id DROP DEFAULT;
       public          zomato_app_3313_user    false    217    216    217            �           2604    16757    reviews review_id    DEFAULT     v   ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);
 @   ALTER TABLE public.reviews ALTER COLUMN review_id DROP DEFAULT;
       public          zomato_app_3313_user    false    226    227    227            �           2604    16659    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          zomato_app_3313_user    false    214    215    215            �          0    16685    menu 
   TABLE DATA           h   COPY public.menu (menu_id, restaurant_id, name, description, price, is_available, category) FROM stdin;
    public          zomato_app_3313_user    false    219   �_       �          0    16737    order_details 
   TABLE DATA           a   COPY public.order_details (order_detail_id, order_id, menu_id, quantity, item_price) FROM stdin;
    public          zomato_app_3313_user    false    225   �j       �          0    16700    orders 
   TABLE DATA           r   COPY public.orders (order_id, user_id, restaurant_id, order_time, delivery_time, status, total_price) FROM stdin;
    public          zomato_app_3313_user    false    221    k       �          0    16720    payments 
   TABLE DATA           �   COPY public.payments (payment_id, order_id, payment_type, transaction_id, payment_status, amount_paid, payment_date) FROM stdin;
    public          zomato_app_3313_user    false    223   Fk       �          0    16670    restaurants 
   TABLE DATA           �   COPY public.restaurants (restaurant_id, owner_user_id, name, restaurant_type, location, rating, is_active, contact_number, description) FROM stdin;
    public          zomato_app_3313_user    false    217   �k       �          0    16754    reviews 
   TABLE DATA           b   COPY public.reviews (review_id, user_id, restaurant_id, rating, comment, review_date) FROM stdin;
    public          zomato_app_3313_user    false    227   io       �          0    16656    users 
   TABLE DATA           �   COPY public.users (user_id, name, username, email, password, phone_number, is_admin, gender, dob, govt_id, bank_details, address) FROM stdin;
    public          zomato_app_3313_user    false    215   �o       �           0    0    menu_menu_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.menu_menu_id_seq', 119, true);
          public          zomato_app_3313_user    false    218            �           0    0 !   order_details_order_detail_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.order_details_order_detail_id_seq', 1, true);
          public          zomato_app_3313_user    false    224            �           0    0    orders_order_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.orders_order_id_seq', 1, true);
          public          zomato_app_3313_user    false    220            �           0    0    payments_payment_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.payments_payment_id_seq', 1, true);
          public          zomato_app_3313_user    false    222            �           0    0    restaurants_restaurant_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.restaurants_restaurant_id_seq', 12, true);
          public          zomato_app_3313_user    false    216            �           0    0    reviews_review_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.reviews_review_id_seq', 1, true);
          public          zomato_app_3313_user    false    226            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 24, true);
          public          zomato_app_3313_user    false    214            �           2606    16693    menu menu_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.menu
    ADD CONSTRAINT menu_pkey PRIMARY KEY (menu_id);
 8   ALTER TABLE ONLY public.menu DROP CONSTRAINT menu_pkey;
       public            zomato_app_3313_user    false    219            �           2606    16742     order_details order_details_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (order_detail_id);
 J   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_pkey;
       public            zomato_app_3313_user    false    225            �           2606    16708    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            zomato_app_3313_user    false    221            �           2606    16730    payments payments_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);
 @   ALTER TABLE ONLY public.payments DROP CONSTRAINT payments_pkey;
       public            zomato_app_3313_user    false    223            �           2606    16678    restaurants restaurants_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (restaurant_id);
 F   ALTER TABLE ONLY public.restaurants DROP CONSTRAINT restaurants_pkey;
       public            zomato_app_3313_user    false    217            �           2606    16763    reviews reviews_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);
 >   ALTER TABLE ONLY public.reviews DROP CONSTRAINT reviews_pkey;
       public            zomato_app_3313_user    false    227            �           2606    16668    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            zomato_app_3313_user    false    215            �           2606    16664    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            zomato_app_3313_user    false    215            �           2606    16666    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            zomato_app_3313_user    false    215            �           2620    16776    orders order_status_trigger    TRIGGER     �   CREATE TRIGGER order_status_trigger BEFORE INSERT ON public.orders FOR EACH ROW EXECUTE FUNCTION public.update_order_status_and_delivery_time();
 4   DROP TRIGGER order_status_trigger ON public.orders;
       public          zomato_app_3313_user    false    229    221            �           2606    16694    menu menu_restaurant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.menu
    ADD CONSTRAINT menu_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);
 F   ALTER TABLE ONLY public.menu DROP CONSTRAINT menu_restaurant_id_fkey;
       public          zomato_app_3313_user    false    219    217    3047            �           2606    16748 (   order_details order_details_menu_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.menu(menu_id);
 R   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_menu_id_fkey;
       public          zomato_app_3313_user    false    225    3049    219            �           2606    16743 )   order_details order_details_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);
 S   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_order_id_fkey;
       public          zomato_app_3313_user    false    221    3051    225            �           2606    16714     orders orders_restaurant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);
 J   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_restaurant_id_fkey;
       public          zomato_app_3313_user    false    221    3047    217            �           2606    16709    orders orders_user_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 D   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_user_id_fkey;
       public          zomato_app_3313_user    false    215    3043    221            �           2606    16731    payments payments_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);
 I   ALTER TABLE ONLY public.payments DROP CONSTRAINT payments_order_id_fkey;
       public          zomato_app_3313_user    false    223    221    3051            �           2606    16679 *   restaurants restaurants_owner_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_owner_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public.users(user_id);
 T   ALTER TABLE ONLY public.restaurants DROP CONSTRAINT restaurants_owner_user_id_fkey;
       public          zomato_app_3313_user    false    215    217    3043            �           2606    16769 "   reviews reviews_restaurant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);
 L   ALTER TABLE ONLY public.reviews DROP CONSTRAINT reviews_restaurant_id_fkey;
       public          zomato_app_3313_user    false    227    3047    217            �           2606    16764    reviews reviews_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 F   ALTER TABLE ONLY public.reviews DROP CONSTRAINT reviews_user_id_fkey;
       public          zomato_app_3313_user    false    3043    215    227                       826    16391     DEFAULT PRIVILEGES FOR SEQUENCES    DEFAULT ACL     [   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO zomato_app_3313_user;
                   postgres    false                       826    16393    DEFAULT PRIVILEGES FOR TYPES    DEFAULT ACL     W   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO zomato_app_3313_user;
                   postgres    false                       826    16392     DEFAULT PRIVILEGES FOR FUNCTIONS    DEFAULT ACL     [   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO zomato_app_3313_user;
                   postgres    false                       826    16390    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     X   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO zomato_app_3313_user;
                   postgres    false            �   =  x��Y�r��>�O1�l%ey��x\j�k�6��ؕ*_����%��g i�'r�!G�X����RW�r�W z���o�Q]����Q���D�UF֪DT:�J_�Y�]*R�k�e$���V��Y�V��㨊��$�F�����$��[��ݾ�֙Ht�QUJBo�.�ǅH�j�_`�J��2	����y4�p��yQ��+�^B�,KpzTվ�o�N��i�=ͼ�Ni�Iz�6�՛�j���,ě�S-n�V�6��(��c5*$�����z��&�� �0��G��m2)>��]A�':Jc��<��#88��M����u0�,̓�V���i�(�u�>Z��*a�yh����s�L2���*iZ�"w��Z��%���F奸K(/U��V�QX�����	֪;2,�1@�A?���[��bW�B�{�槈�l7��+Hi�Ι���t� )���F�@��Ђ;����E���E��h�B2�ъ�3�[�*��J7>b�#�d�����9����f� ���1�\��,
R( M%rJ���Z7J�v+�V��[��]̓MȔ7������LGq���Q�C���rT	�A�d��)�+����;!<��m��[0�D�h��A4a��l4D�� �V�7����hS��/�݋�N�rą�M]t��qF�)��;%�7b�у6�м��m����[~& /��l9u4��1�w���x�|���Ƨ2��"�}�sO�f����%�F� ��
"��!�H�LE�F���r4�{�C����c����'�^�[�|�8i�Y��cc��h,l��h69^ ��J���g�JnO����E�n3�2��2z�����ɒ�$���Rb�3�+��w>���a/�%U^͞�w�,��ۋQ�6�4�O.��\A��ɡ"��ќ�=�J�R+�Z�!cN��
���T^4榬��y��Z"y�w�bP�E!9�JgQ��sX��s��*\�����Y����u4]��M�l۽Nt
��h���-2C*�=i?�SE��J����f�UT(v�U9�ta�$�i�w�V���ğ-��.(�#�� ������Q�j��T�]�o8]��.�N�e�ݶ�q��jCYv��CH	Ԝ���d\�FӐ��5!�k�t�ϟ���8BNo���^����i�S��6n�x< ��������Qnh�@�W�9����Ҡ��)j\�+�AC��RO��W �/q��=*��B�W(g�^����{�QJD,��+��9�X}��q�cqp{�رb��p�hMf#����8��8�� ek�~2O~�$�%�c<?��;v �(�+r]�K�>s���UxЏ8��r�G��񙚫�!��{�\����oĵ�*��7p
�77�ǉ�����=���O�����f��}�U�P��G�p>R��s<�y_g�(���}�L�_�>FrH�=q�C՞ܫ����7T�6LND��G"��(G}_�)� �>���c;?�9qo3]�P:�vU�|4�>lF3׈t����9�y�=�g"n��u����Z�p�ĵX���^���g���]o�z�y\�㴀����3�Zq�����Ja�Wb��.1�q�� ������1M�8x�&���CJy�y�)W�p,�������|qt^���8:�h�Լ�nIu�=��yzt�mNǓ��]��\ᚭ�ǁ�Ť#�?G�N 7+>�m�[��Kj.�A{�y�܁�;��S	�Y��Q�:�o1����1~�x������څ�g�o�ud�8D�~x�rW�DQ6�/;���_>��(���|�2���8=5}�Ԃ-y���P��qqs���}�����Q�J4�2횏�����4S�c���Z��������E<=p��s^��^7�-����
;����i٦؋�\/�)W峬��q�.x���ϩ��K��h���m�FE\�����澰s����P�/_�V�hG�%#���'��i�)��_��#�x4Μ�P�<ߕ���T���K�~���فQZ�F�0�	~�W@C��T�5�x��7�<,�{0��<A�p�S_��e}��b u3��V;�%uR��o���!Ȉk��Վp� �_m�][��6T+ǀ�D�F�?��"�W���l7L��
h|�DՓ:����#�\�\k\!��Y�K�>b����$Z��;��J�W����3S3+�7,#�zD���S�58ҺBI;��OGZ?u���Z�J��7p�F�p�'�f ����8i|���2
��a� �V.\7F�/RЁ�2C���Z������j�v�� Ε�E2�*Z%t�´�.�H��bY�-�� hc<�ߙ0В��o�b(_����anj��Im��@�Raz��&��wg��
�c�q��wN�f������QYۺP����E���:6lT��0Gٸ���_�6���z#~2T���D�Y��-�xu�l�|�[a��%A��!��1���Z�1�zg�j�ҺB�#<w�PZ�� �'��4��߂�1�C̃+�w�c���eK��/h�O����"�'8���.�;�����sC`�)C�����jG��9���"��<�����g�(�g G=�}�v�wȮ[�.w���3�.�z��ʤrմ�ّ��p��Am��!�O�3�+������Ʋ�����=�6�Q=ܦ����\�$n>)UF[��'�$^0�s���?�Cf'����ݠ|��������њS�=���g�U&v��i˙��6��u��5
�8�1�p����S��;|���l*�:K_���5;FZ1����u&C٢�P�C�ѫ����	l�d�G�܌fg�����h�o+W�      �      x�3�4C3KK=�=... ��      �   6   x�3�4B##]c]#KC#+ ���H�K��K�4���30������ �b	�      �   M   x��1�  ��}��i�f��nD'���{' p��	��Tk�b��D��s'fP֒8'���m�JUԽ�M��4�      �   �  x�e�Mr�6���):�TM�*R�Z���x천�ƛ6�21�@ Z#U�F���䁶~f� E�@�ׯ_+U}u��{�{6��*� F��ݲ��N$�ao���f��x4��D]�T�'�-T[�[���j���?=�+^����"{��6[<�e���xå�^c>U�l~�k��[�;��Z���4�`\4Ae��EVU��o^���Pqѥoڗ[^��0}�WvXbϚ� zx��]�0L�~���28�ҍ-4��um�W;:f���<bt��Ɠ��{��8PSCz�=$�'��2j����W����G,�_t�
qd�-�-�U���+��,Z�ӟ�>�DV9�TN�7yI��}�Z�V8E�l�jm��B�_��P(��O\GȂwu�ҁ�D���Y����3LQL��_�����Zk5�͢6��`<�����#6G��;'rZTUH΅tF*������=}�V\�@j]v���uiY;��b
8nS�F�l�9��行!��o�5��i��{��})���t�������9�۩E[�p4�k�9&~�o⢇F�iG��4��G61���8������trí�᫜QLT:VW%$U]�G;�m2���5����m�K�Z�.��^UsK7��F�GiYZ��:�0M�<@��rk��K��T�u�n�̗�pչ�I
wX9ʰ���L � �<
@ ����6����9x�<�?S�ݷ�hl?�z/�'6�<�~�9R��Prl<ugzc�%��NM�8��y�Q�L�s�/4#{��� (���`wr������ � V��fw�BZ[�]+pG[0����{1�]�ȅ�׀�,��'�KUZp|��g><�և�� � PWuc���D����{����g�z 0�ѭ�y�srH_ah!��9�����];��7��a��/Sq=�]��NSq���h�2o�7e���t:���      �   I   x�3�4BSN������̪�D�ļ�Ԋ�Ԝ�Լ��Ԣ���TEN##]c]#KCc+ ����� �%�      �   o  x���Ys�<���_��8	��e�NU�n�l�ʍ��c����O2p53u2s�*$��<y[�n�3����p��37܌cy�ʽ�
�o�$��I�N��S+�o	BA���~�~�cɒj�<�׺E>��q/�+�P]ڬ��5k0�iK(���16��s/��v^m��9
�"�dEe��u���+ˑ��Vo0u��m�I�8g�ɿ�?�����13%0 Q����}�Y�7
��ح��i^y��ƕ�?�;�
a����iu<@��L۱ak��n��RvgQ�@Ud	�ϱ ��)����X��ܟN �`�e�(�18f��D&|�l�ڏ�3���M/n/ՁV�uvt���}_���[;u;[��O�0�����RqY�ݡd��R���p��gY���)�ǐ~��	G�c;p\�3IR�	�(F��_��,t0�����޵�o�����'��R���5ag�:V�X[�;�흎�J��>��0�	]ՙg��:�r;8�@�"I��><ˋ����	@ӻ��Z�2���e���u�&���QYTr���̬�]��zR~_�yuT;+_�f��?7��a�+��%���
��6�V?4�,���\9�*\�{:����A�w�x��*�!L,S&�P�&���3D:��J���8e?�Ж1\�#�%��!]e�eVaV�>��
g#�5;�u:��<��~E5����b8�$6��:R6r�=	k�קy��Mv:�S�@I���	]ۍn|Rɧ��gS/���>��P��,'���(����L��PJ\�qVڥ��]�̫ΔN&�~/�t:��[�ce��ƚ�q#%�6'M�eە?���csvq�&��~�J	�V�O�ǀ��Nz��B�m�"PdQUN9��ʹ{m[j��t��C����A�?j��	YP������7�s^ǅ֯�ݭy�i\q�NVoL�n�l�EK{vr�e�i&z?�3�-u�ׇ�r��P"a��C�#��D�甞���O�@mQ?2#"����~w���r�՘g��\l�o�i�ic��[��R͙ܰB}g��,O!�`�1��0v��n�P$r�X2R��Ͷ&¶�A**�<���݆mj6S7u�[�x�L���v�S���/���8	�Y�N���\zwO(�mݟ"�x^D���{�Rb��v�{}� /J
�	PfT��*�(��Ak\���1�A�&@��/�f���lw2I"l��rՓ�����Z��ʔ�28Fa�2��$����d�ݔ1P��{����ir;�ÜwJY~А�W�f�Q	�r<C$T)��H�MC�|)=3]7�Q�>�q������Hw Ey�Ny%��ز'%��a(c	����$;�䔓�}�k?�tR��H�Ti���拒G�,�^%�
F(Or��N_����m���n[?wGc�G����$�,WZ����3Y�\����J�4��F+�����~�D���׀�%*Po4[%�o.H�|#�`��s��kt�_K����_�׿GzR�]��c=Ǩ,��Q`�� ���dxϊ8"��-BY���o$�s;~~�]N\˗�DnxҸbo�pn�?�=}??V-5�{�:�&��Jb=c&t�h�yG�|}e�<��1c���N�|�ek��HU�d����H�Erd�&$� ��Ǥ��/sO�b�����w���7��k����(��Z��Ko�o�R�I�w�R��p�\�y}ͬ�:#�՚�r�~M�V��,K�W�)%�=��s�r?�~�$*'�d�ܡ��Dkc�t� ڞ��!�ʂ��G8ݷ�\���y�+�bۨo�[���WOƢ1?���]3��W��ɧA+IZ�<�+�����1]�GN@S� �`�� :�
Le��<�az����������A     