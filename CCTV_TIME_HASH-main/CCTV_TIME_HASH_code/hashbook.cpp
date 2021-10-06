#include <eosio/eosio.hpp>

using namespace eosio;

class [[eosio::contract("hashbook")]] hashbook : public eosio::contract {
        public:

        private:
                struct [[eosio::table]] hash {
                uint64_t time;
                std::string hash;

                uint64_t primary_key() const { return time; }
        };

        using hash_index = eosio::multi_index<"hashes"_n, hash>;

        public:
                hashbook(name receiver, name code, datastream<const char*> ds): contract(receiver, code, ds) {} //code - 컨트랙트의 계정, 액션을 실행하는 계정


                [[eosio::action]]
                void insert(
                        name user,
                        uint64_t time,
                        std::string hash
                ){

                        require_auth(user);
                        hash_index hash_table(get_self(), get_first_receiver().value);

                        hash_table.emplace(user, [&](auto&row){
                                row.time = time;
                                row.hash = hash;
                        });
                }
};

